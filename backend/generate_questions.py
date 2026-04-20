#!/usr/bin/env python3
"""
Master question generation script for SOA exams.

Generates 50K+ questions across all SOA exams by:
1. Loading all exam generators
2. Getting all methods from each generator
3. Generating N variants per method with different random seeds
4. Saving questions as JSON files organized by exam
5. Providing detailed statistics and validation
"""

import argparse
import json
import os
import sys
import uuid
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

from app.services.generators import ALL_GENERATORS


class QuestionGenerator:
    """Master question generator that orchestrates all exam generators."""

    # Expected method counts per exam (used for statistics)
    EXPECTED_METHOD_COUNTS = {
        "P": 95,
        "FM": 70,
        "FAM": 70,
        "ALTAM": 52,
        "ASTAM": 50,
        "SRM": 60,
        "PA": 50,
    }

    def __init__(
        self,
        variants_per_method: int = 120,
        output_dir: str = "./output/questions",
        exam: Optional[str] = None,
    ):
        """
        Initialize the question generator.

        Args:
            variants_per_method: Number of question variants to generate per method
            output_dir: Directory to save output JSON files
            exam: If specified, only generate for this exam (e.g., "P", "FM")
        """
        self.variants_per_method = variants_per_method
        self.output_dir = Path(output_dir)
        self.exam_filter = exam
        self.questions_by_exam = defaultdict(list)
        self.questions_by_topic = defaultdict(lambda: defaultdict(int))
        self.difficulty_distribution = defaultdict(lambda: defaultdict(int))
        self.errors = []

    def validate_question(self, question: Dict[str, Any], exam: str) -> bool:
        """
        Validate that a question has all required fields.

        Args:
            question: Question dictionary to validate
            exam: Exam code

        Returns:
            True if valid, False otherwise
        """
        required_fields = {"id", "exam", "topic", "difficulty", "question", "options"}

        if not isinstance(question, dict):
            return False

        missing_fields = required_fields - set(question.keys())
        if missing_fields:
            self.errors.append(
                f"Question missing fields {missing_fields}: {question.get('id', 'unknown')}"
            )
            return False

        # Validate field types and values
        if not isinstance(question["id"], str) or not question["id"]:
            self.errors.append(f"Invalid question ID: {question.get('id')}")
            return False

        if question["exam"] != exam:
            self.errors.append(
                f"Question exam mismatch: expected {exam}, got {question['exam']}"
            )
            return False

        if question["difficulty"] not in ["easy", "medium", "hard"]:
            self.errors.append(
                f"Invalid difficulty: {question.get('difficulty')}"
            )
            return False

        if not isinstance(question.get("options"), list) or len(question["options"]) < 2:
            self.errors.append(
                f"Invalid options for question {question.get('id')}"
            )
            return False

        return True

    def generate_for_exam(self, exam_code: str) -> int:
        """
        Generate questions for a specific exam.

        Args:
            exam_code: Exam code (e.g., "P", "FM")

        Returns:
            Total number of questions generated
        """
        if exam_code not in ALL_GENERATORS:
            print(f"ERROR: Unknown exam code '{exam_code}'")
            return 0

        generator_class = ALL_GENERATORS[exam_code]
        generator = generator_class()

        try:
            methods = generator.get_all_methods()
        except Exception as e:
            print(f"ERROR: Failed to get methods for {exam_code}: {e}")
            return 0

        print(f"\n{'=' * 70}")
        print(f"Generating questions for Exam {exam_code}")
        print(f"{'=' * 70}")
        print(f"Found {len(methods)} methods")
        print(f"Generating {self.variants_per_method} variants per method")
        expected_total = len(methods) * self.variants_per_method
        print(f"Expected questions: {expected_total:,}")
        print(f"{'=' * 70}")

        questions_generated = 0
        questions_skipped = 0

        for idx, method_name in enumerate(methods, 1):
            # Progress indicator
            progress = f"[{idx}/{len(methods)}]"
            print(f"{progress} {method_name:<50}", end="", flush=True)

            method_success_count = 0

            for variant in range(self.variants_per_method):
                try:
                    # Use variant number as part of the random seed for diversity
                    question = generator.generate(
                        method_name=method_name,
                        random_seed=variant,
                    )

                    # Add unique ID if not present
                    if "id" not in question or not question["id"]:
                        question["id"] = str(uuid.uuid4())

                    # Add generation metadata
                    question["generated_at"] = datetime.utcnow().isoformat()
                    question["variant"] = variant

                    # Validate question
                    if self.validate_question(question, exam_code):
                        self.questions_by_exam[exam_code].append(question)
                        self.questions_by_topic[exam_code][question.get("topic", "Unknown")] += 1
                        self.difficulty_distribution[exam_code][
                            question.get("difficulty", "medium")
                        ] += 1
                        method_success_count += 1
                        questions_generated += 1
                    else:
                        questions_skipped += 1

                except Exception as e:
                    questions_skipped += 1
                    # Don't spam output with every error, but track them
                    if questions_skipped < 10:  # Only show first few errors
                        self.errors.append(
                            f"Error generating variant {variant} for {exam_code}.{method_name}: {str(e)[:100]}"
                        )

            # Print result for this method
            success_rate = (
                f"{method_success_count}/{self.variants_per_method}"
            )
            print(f" {success_rate:<15} OK")

        print(f"\n{'-' * 70}")
        print(f"Exam {exam_code} Summary:")
        print(f"  Questions generated: {questions_generated:,}")
        print(f"  Questions skipped: {questions_skipped:,}")
        print(f"  Success rate: {questions_generated / (questions_generated + questions_skipped) * 100:.1f}%")

        return questions_generated

    def save_exam_json(self, exam_code: str) -> str:
        """
        Save questions for a specific exam to JSON file.

        Args:
            exam_code: Exam code

        Returns:
            Path to saved file
        """
        questions = self.questions_by_exam[exam_code]
        output_file = self.output_dir / f"exam_{exam_code.lower()}.json"

        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, "w") as f:
            json.dump(
                {
                    "exam": exam_code,
                    "count": len(questions),
                    "generated_at": datetime.utcnow().isoformat(),
                    "questions": questions,
                },
                f,
                indent=2,
            )

        return str(output_file)

    def save_combined_json(self) -> str:
        """
        Save all questions to a combined JSON file.

        Returns:
            Path to saved file
        """
        all_questions = []
        for exam_code in sorted(self.questions_by_exam.keys()):
            all_questions.extend(self.questions_by_exam[exam_code])

        output_file = self.output_dir / "all_questions.json"
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, "w") as f:
            json.dump(
                {
                    "total": len(all_questions),
                    "exams": list(self.questions_by_exam.keys()),
                    "generated_at": datetime.utcnow().isoformat(),
                    "questions": all_questions,
                },
                f,
                indent=2,
            )

        return str(output_file)

    def print_summary(self):
        """Print detailed summary statistics."""
        print(f"\n{'=' * 70}")
        print("SUMMARY STATISTICS")
        print(f"{'=' * 70}\n")

        total_questions = 0

        # Per-exam statistics
        print("Questions per exam:")
        print(f"{'-' * 70}")
        for exam in sorted(self.questions_by_exam.keys()):
            count = len(self.questions_by_exam[exam])
            expected = self.EXPECTED_METHOD_COUNTS.get(exam, "?")
            pct = f"({count / expected * 100:.1f}% of expected)" if isinstance(
                expected, int
            ) else ""
            print(f"  {exam:<10} {count:>6,} questions  {pct}")
            total_questions += count

        print(f"{'-' * 70}")
        print(f"  {'TOTAL':<10} {total_questions:>6,} questions")

        # Per-topic statistics (sample from first exam)
        if self.questions_by_exam:
            first_exam = sorted(self.questions_by_exam.keys())[0]
            print(f"\n\nTopics in Exam {first_exam}:")
            print(f"{'-' * 70}")
            for topic, count in sorted(
                self.questions_by_topic[first_exam].items(), key=lambda x: -x[1]
            )[:10]:
                print(f"  {topic:<40} {count:>6,} questions")
            if len(self.questions_by_topic[first_exam]) > 10:
                remaining = sum(
                    count
                    for topic, count in self.questions_by_topic[first_exam].items()
                    if topic
                    not in sorted(
                        self.questions_by_topic[first_exam].items(), key=lambda x: -x[1]
                    )[:10]
                )
                print(f"  {'(other topics)':<40} {remaining:>6,} questions")

        # Difficulty distribution
        print(f"\n\nDifficulty distribution:")
        print(f"{'-' * 70}")
        for exam in sorted(self.questions_by_exam.keys()):
            print(f"\nExam {exam}:")
            total = len(self.questions_by_exam[exam])
            for difficulty in ["easy", "medium", "hard"]:
                count = self.difficulty_distribution[exam].get(difficulty, 0)
                pct = (count / total * 100) if total > 0 else 0
                print(
                    f"  {difficulty:<10} {count:>6,} ({pct:>5.1f}%)"
                )

        # Errors summary
        if self.errors:
            print(f"\n\nErrors encountered: {len(self.errors)}")
            print(f"{'-' * 70}")
            for error in self.errors[:10]:
                print(f"  - {error}")
            if len(self.errors) > 10:
                print(f"  ... and {len(self.errors) - 10} more errors")

        print(f"\n{'=' * 70}\n")

    def generate(self) -> int:
        """
        Generate all questions.

        Returns:
            Total number of questions generated
        """
        exams_to_generate = [self.exam_filter] if self.exam_filter else list(
            ALL_GENERATORS.keys()
        )

        total_generated = 0

        for exam in sorted(exams_to_generate):
            try:
                count = self.generate_for_exam(exam)
                total_generated += count
            except Exception as e:
                print(f"\nFATAL ERROR generating {exam}: {e}")
                import traceback
                traceback.print_exc()
                continue

        # Save results
        print(f"\n{'=' * 70}")
        print("Saving results...")
        print(f"{'=' * 70}")

        for exam in sorted(self.questions_by_exam.keys()):
            output_file = self.save_exam_json(exam)
            print(f"Saved {exam:<10} -> {output_file}")

        combined_file = self.save_combined_json()
        print(f"Saved combined  -> {combined_file}")

        # Print summary
        self.print_summary()

        return total_generated


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate 50K+ SOA exam questions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_questions.py                    # Generate all exams
  python generate_questions.py --exam P           # Generate only Exam P
  python generate_questions.py --variants-per-method 200  # More variants
  python generate_questions.py --output-dir /tmp/questions  # Custom output
        """,
    )

    parser.add_argument(
        "--variants-per-method",
        type=int,
        default=120,
        help="Number of variants to generate per method (default: 120)",
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        default="./output/questions",
        help="Output directory for JSON files (default: ./output/questions)",
    )

    parser.add_argument(
        "--exam",
        type=str,
        choices=["P", "FM", "FAM", "ALTAM", "ASTAM", "SRM", "PA"],
        help="Generate only for specific exam (default: all exams)",
    )

    args = parser.parse_args()

    print("\n")
    print("=" * 70)
    print("SOA EXAM QUESTION GENERATOR")
    print("=" * 70)
    print(f"Variants per method: {args.variants_per_method}")
    print(f"Output directory: {args.output_dir}")
    if args.exam:
        print(f"Exam filter: {args.exam}")
    print("=" * 70)
    print()

    generator = QuestionGenerator(
        variants_per_method=args.variants_per_method,
        output_dir=args.output_dir,
        exam=args.exam,
    )

    try:
        total = generator.generate()
        print(f"\nGeneration complete! Total questions: {total:,}")
        return 0
    except KeyboardInterrupt:
        print("\n\nGeneration cancelled by user")
        return 1
    except Exception as e:
        print(f"\n\nFATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
