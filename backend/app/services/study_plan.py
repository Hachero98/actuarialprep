"""
Study plan generation using adaptive scheduling and spaced repetition.

Generates personalized study plans that allocate time to weak topics with consideration
for exam importance weights and uses spaced repetition for long-term retention.
"""

from typing import Dict, List
from datetime import datetime, timedelta
import math


class StudyPlanGenerator:
    """
    Generate adaptive study plans using topic prioritization and spaced repetition.
    """

    # Spaced repetition intervals (in days)
    SPACED_REPETITION_INTERVALS = [1, 3, 7, 14, 30]

    def __init__(self):
        """Initialize the study plan generator."""
        pass

    def calculate_topic_priority(
        self,
        mastery: float,
        weight: float,
        priority_curve: str = "sqrt"
    ) -> float:
        """
        Calculate priority score for a topic based on mastery and exam importance.

        Priority indicates how urgently a topic needs study.
        Formula: priority = weight * (1 - mastery)^curve_factor

        The curve parameter allows for different prioritization strategies:
        - "linear": priority = weight * (1 - mastery)
        - "sqrt": priority = weight * sqrt(1 - mastery)  [default, smoother]
        - "square": priority = weight * (1 - mastery)^2

        Args:
            mastery: Current mastery level (0-1).
            weight: Exam syllabus weight for this topic (typically 0-1 or 0-100).
            priority_curve: Type of priority curve to use.

        Returns:
            Priority score (higher = more urgent to study).
        """
        gap = 1.0 - mastery

        if priority_curve == "linear":
            priority = weight * gap
        elif priority_curve == "square":
            priority = weight * (gap ** 2)
        else:  # "sqrt" (default)
            priority = weight * math.sqrt(gap)

        return float(priority)

    def schedule_reviews(
        self,
        topics: List[Dict],
        start_date: str,
        end_date: str = None
    ) -> List[Dict]:
        """
        Schedule review sessions for topics using spaced repetition intervals.

        Spaced repetition: review a topic at 1, 3, 7, 14, 30 day intervals
        to optimally consolidate long-term memory.

        Args:
            topics: List of topic dicts with keys:
                - 'id': str, topic identifier
                - 'mastery': float, current mastery (0-1)
                - 'weight': float, exam weight
            start_date: Start date as "YYYY-MM-DD" string.
            end_date: End date as "YYYY-MM-DD" string (optional).

        Returns:
            List of review schedules, each dict with keys:
                - 'topic_id': str
                - 'review_date': str, "YYYY-MM-DD" format
                - 'review_number': int, 1-5 corresponding to interval
                - 'interval_days': int
        """
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Invalid start_date format: {start_date}. Use YYYY-MM-DD.")

        if end_date:
            try:
                end = datetime.strptime(end_date, "%Y-%m-%d")
            except ValueError:
                raise ValueError(f"Invalid end_date format: {end_date}. Use YYYY-MM-DD.")
        else:
            # Default to 60 days of planning
            end = start + timedelta(days=60)

        reviews = []

        for topic in topics:
            topic_id = topic.get('id', 'unknown')

            for review_num, interval_days in enumerate(self.SPACED_REPETITION_INTERVALS, 1):
                review_date = start + timedelta(days=interval_days)

                # Only schedule if within planning window
                if review_date <= end:
                    reviews.append({
                        'topic_id': topic_id,
                        'review_date': review_date.strftime("%Y-%m-%d"),
                        'review_number': review_num,
                        'interval_days': interval_days,
                    })

        return reviews

    def generate_plan(
        self,
        user_mastery: Dict[str, float],
        exam_weights: Dict[str, float],
        days_until_exam: int,
        hours_per_day: float = 2.0,
        start_date: str = None
    ) -> Dict:
        """
        Generate a day-by-day study plan allocating time to weak topics.

        The plan prioritizes topics based on (1) how weak they are and (2) their
        exam importance. More time is allocated to high-priority topics.
        Includes scheduled reviews using spaced repetition.

        Args:
            user_mastery: Dict mapping topic_id -> mastery (0-1).
            exam_weights: Dict mapping topic_id -> weight (typically 0-1 or 0-100).
            days_until_exam: Number of days remaining until exam.
            hours_per_day: Daily study hours available (default 2.0).
            start_date: Plan start date as "YYYY-MM-DD" (default: today).

        Returns:
            Study plan dict with keys:
                - 'start_date': str, YYYY-MM-DD format
                - 'end_date': str, YYYY-MM-DD format
                - 'exam_date': str, YYYY-MM-DD format
                - 'total_study_hours': float
                - 'days_available': int
                - 'hours_per_day': float
                - 'topic_allocations': list of dicts with topic_id, hours, daily_hours, priority
                - 'daily_schedule': list of dicts with date, topics and hours
                - 'review_schedule': list of review sessions
        """
        if start_date is None:
            start_date = datetime.now().strftime("%Y-%m-%d")

        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Invalid start_date format: {start_date}. Use YYYY-MM-DD.")

        end_date = start + timedelta(days=days_until_exam - 1)
        exam_date = start + timedelta(days=days_until_exam)

        # Calculate topic priorities
        topic_priorities = []
        total_priority = 0.0

        for topic_id, weight in exam_weights.items():
            mastery = user_mastery.get(topic_id, 0.0)
            priority = self.calculate_topic_priority(mastery, weight)
            total_priority += priority

            topic_priorities.append({
                'topic_id': topic_id,
                'mastery': mastery,
                'weight': weight,
                'priority': priority,
            })

        # Sort by priority (descending)
        topic_priorities.sort(key=lambda x: x['priority'], reverse=True)

        # Allocate study hours based on priority
        total_hours = days_until_exam * hours_per_day
        topic_allocations = []

        for topic_data in topic_priorities:
            if total_priority > 0:
                proportion = topic_data['priority'] / total_priority
            else:
                proportion = 1.0 / len(topic_priorities)

            allocated_hours = total_hours * proportion

            topic_allocations.append({
                'topic_id': topic_data['topic_id'],
                'mastery': topic_data['mastery'],
                'weight': topic_data['weight'],
                'priority': topic_data['priority'],
                'total_hours_allocated': float(allocated_hours),
                'daily_hours': float(allocated_hours / days_until_exam),
            })

        # Build daily schedule
        daily_schedule = []
        day_idx = 0

        while day_idx < days_until_exam:
            current_date = start + timedelta(days=day_idx)
            day_date = current_date.strftime("%Y-%m-%d")

            # Topics for this day (rotate through high-priority topics)
            day_topics = []
            remaining_hours = hours_per_day

            for topic_alloc in topic_allocations:
                daily_hours = topic_alloc['daily_hours']

                if remaining_hours >= daily_hours * 0.5:  # At least 50% of allocation
                    day_topics.append({
                        'topic_id': topic_alloc['topic_id'],
                        'hours': min(daily_hours, remaining_hours),
                    })
                    remaining_hours -= day_topics[-1]['hours']

            daily_schedule.append({
                'date': day_date,
                'day_number': day_idx + 1,
                'topics': day_topics,
                'total_hours': hours_per_day,
            })

            day_idx += 1

        # Generate review schedule
        review_topics = [
            {'id': t['topic_id'], 'mastery': t['mastery'], 'weight': t['weight']}
            for t in topic_allocations
        ]
        review_schedule = self.schedule_reviews(
            review_topics,
            start_date=start_date,
            end_date=end_date.strftime("%Y-%m-%d")
        )

        return {
            'start_date': start_date,
            'end_date': end_date.strftime("%Y-%m-%d"),
            'exam_date': exam_date.strftime("%Y-%m-%d"),
            'total_study_hours': float(total_hours),
            'days_available': days_until_exam,
            'hours_per_day': float(hours_per_day),
            'topic_allocations': topic_allocations,
            'daily_schedule': daily_schedule,
            'review_schedule': review_schedule,
        }

    def get_recommended_topics_for_day(
        self,
        daily_plan: Dict,
        optional_reviews: List[Dict] = None
    ) -> Dict:
        """
        Get recommended topics and reviews for a specific day.

        Useful for real-time recommendation during study sessions.

        Args:
            daily_plan: Single day's plan dict from generate_plan's daily_schedule.
            optional_reviews: Optional list of review schedules to check for today.

        Returns:
            Dict with:
                - 'primary_topics': list of main topics to study
                - 'review_topics': list of topics due for review
                - 'total_hours': float
                - 'recommended_order': list of (topic_id, hours) tuples
        """
        primary_topics = daily_plan.get('topics', [])

        reviews_today = []
        if optional_reviews:
            today = daily_plan.get('date')
            reviews_today = [
                r for r in optional_reviews
                if r.get('review_date') == today
            ]

        return {
            'primary_topics': [t['topic_id'] for t in primary_topics],
            'review_topics': [r['topic_id'] for r in reviews_today],
            'total_hours': daily_plan.get('total_hours', 0),
            'recommended_order': [
                (t['topic_id'], t['hours']) for t in primary_topics
            ],
            'reviews_due': len(reviews_today),
        }
