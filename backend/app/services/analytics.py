"""
Analytics service for progress tracking, performance analysis, and pass probability prediction.

Provides comprehensive learning analytics including performance summaries, topic breakdowns,
and predictive modeling for exam readiness.
"""

from typing import Dict, List, Optional
import statistics
import math


class AnalyticsService:
    """
    Analytics service for tracking learning progress and predicting exam readiness.
    """

    # Logistic regression parameters for pass probability prediction
    # Based on historical passing data
    PASS_PROBABILITY_INTERCEPT = -4.5
    PASS_PROBABILITY_SLOPE = 0.08  # per point of readiness score

    def __init__(self):
        """Initialize the analytics service."""
        pass

    def get_progress_summary(self, performances: List[Dict]) -> Dict:
        """
        Compute overall progress summary from response history.

        Tracks:
        - Total questions attempted
        - Accuracy rate (overall and recent)
        - Average response time
        - Current streak
        - Trend (improving, stable, declining)

        Args:
            performances: List of performance dicts with keys:
                - 'is_correct': bool
                - 'response_time_seconds': float
                - 'timestamp': str, ISO format (optional)
                - 'difficulty': float, 0-1 (optional)
                - 'topic': str (optional)

        Returns:
            Progress summary dict with keys:
                - 'total_questions': int
                - 'correct_count': int
                - 'accuracy_rate': float, 0-1
                - 'recent_accuracy': float (last 20 questions)
                - 'average_response_time': float, seconds
                - 'current_streak': int
                - 'longest_streak': int
                - 'trend': str, "improving", "stable", or "declining"
                - 'improvement_rate': float
        """
        if not performances:
            return {
                'total_questions': 0,
                'correct_count': 0,
                'accuracy_rate': 0.0,
                'recent_accuracy': 0.0,
                'average_response_time': 0.0,
                'current_streak': 0,
                'longest_streak': 0,
                'trend': 'stable',
                'improvement_rate': 0.0,
            }

        total = len(performances)
        correct = sum(1 for p in performances if p.get('is_correct', False))
        accuracy = correct / total if total > 0 else 0.0

        # Recent accuracy (last 20 questions)
        recent_count = min(20, total)
        recent_correct = sum(
            1 for p in performances[-recent_count:]
            if p.get('is_correct', False)
        )
        recent_accuracy = recent_correct / recent_count if recent_count > 0 else 0.0

        # Response times
        times = [p.get('response_time_seconds', 0) for p in performances]
        avg_time = statistics.mean(times) if times else 0.0

        # Streaks
        current_streak = 0
        longest_streak = 0

        for perf in performances:
            if perf.get('is_correct', False):
                current_streak += 1
                longest_streak = max(longest_streak, current_streak)
            else:
                current_streak = 0

        # Trend: compare first half to second half
        half_point = total // 2
        first_half_acc = sum(
            1 for p in performances[:half_point]
            if p.get('is_correct', False)
        ) / half_point if half_point > 0 else 0.0

        second_half_acc = sum(
            1 for p in performances[half_point:]
            if p.get('is_correct', False)
        ) / (total - half_point) if half_point < total else 0.0

        improvement_rate = second_half_acc - first_half_acc

        if improvement_rate > 0.05:
            trend = "improving"
        elif improvement_rate < -0.05:
            trend = "declining"
        else:
            trend = "stable"

        return {
            'total_questions': total,
            'correct_count': correct,
            'accuracy_rate': float(accuracy),
            'recent_accuracy': float(recent_accuracy),
            'average_response_time': float(avg_time),
            'current_streak': current_streak,
            'longest_streak': longest_streak,
            'trend': trend,
            'improvement_rate': float(improvement_rate),
        }

    def get_topic_breakdown(
        self,
        performances: List[Dict],
        topics: List[str]
    ) -> List[Dict]:
        """
        Compute per-topic performance metrics.

        For each topic:
        - Accuracy rate
        - Average response time
        - Estimated mastery level
        - Sample size

        Args:
            performances: List of performance dicts (must include 'topic' key).
            topics: List of topic identifiers to analyze.

        Returns:
            List of topic breakdowns, each dict with:
                - 'topic': str
                - 'question_count': int
                - 'correct_count': int
                - 'accuracy': float, 0-1
                - 'average_response_time': float, seconds
                - 'mastery_level': str, "novice", "developing", "proficient", "expert"
                - 'mastery_score': float, 0-1
                - 'confidence_interval': dict with 'lower' and 'upper'
        """
        breakdown = []

        for topic in topics:
            topic_perfs = [
                p for p in performances
                if p.get('topic') == topic
            ]

            if not topic_perfs:
                breakdown.append({
                    'topic': topic,
                    'question_count': 0,
                    'correct_count': 0,
                    'accuracy': 0.0,
                    'average_response_time': 0.0,
                    'mastery_level': 'not_attempted',
                    'mastery_score': 0.0,
                    'confidence_interval': {'lower': 0.0, 'upper': 0.0},
                })
                continue

            count = len(topic_perfs)
            correct = sum(1 for p in topic_perfs if p.get('is_correct', False))
            accuracy = correct / count if count > 0 else 0.0

            times = [p.get('response_time_seconds', 0) for p in topic_perfs]
            avg_time = statistics.mean(times) if times else 0.0

            # Mastery level classification
            if accuracy >= 0.9:
                mastery_level = "expert"
            elif accuracy >= 0.75:
                mastery_level = "proficient"
            elif accuracy >= 0.5:
                mastery_level = "developing"
            else:
                mastery_level = "novice"

            # Confidence interval (Wilson score interval)
            ci = self._wilson_confidence_interval(correct, count, confidence=0.95)

            breakdown.append({
                'topic': topic,
                'question_count': count,
                'correct_count': correct,
                'accuracy': float(accuracy),
                'average_response_time': float(avg_time),
                'mastery_level': mastery_level,
                'mastery_score': float(accuracy),
                'confidence_interval': {
                    'lower': float(ci[0]),
                    'upper': float(ci[1]),
                },
            })

        # Sort by accuracy
        breakdown.sort(key=lambda x: x['accuracy'])

        return breakdown

    def predict_pass_probability(
        self,
        readiness_score: float,
        historical_data: Optional[Dict] = None
    ) -> Dict:
        """
        Predict probability of passing the exam using logistic model.

        The logistic model maps readiness scores (0-100) to pass probability (0-1)
        based on historical passing data.

        Model: P(pass) = 1 / (1 + exp(-(intercept + slope * readiness)))

        Args:
            readiness_score: Readiness score (typically 0-100).
            historical_data: Optional historical calibration data with keys:
                - 'intercept': float
                - 'slope': float
                - 'historical_accuracy': float

        Returns:
            Dict with keys:
                - 'pass_probability': float, 0-1
                - 'confidence_level': str, "low", "moderate", "high"
                - 'estimated_performance': str, "likely_fail", "borderline", "likely_pass"
                - 'recommendation': str
        """
        # Use provided historical data or defaults
        if historical_data:
            intercept = historical_data.get('intercept', self.PASS_PROBABILITY_INTERCEPT)
            slope = historical_data.get('slope', self.PASS_PROBABILITY_SLOPE)
        else:
            intercept = self.PASS_PROBABILITY_INTERCEPT
            slope = self.PASS_PROBABILITY_SLOPE

        # Logistic function
        exponent = intercept + slope * readiness_score
        # Clip to avoid overflow
        exponent = max(min(exponent, 100), -100)
        pass_prob = 1.0 / (1.0 + math.exp(-exponent))

        # Confidence level based on readiness
        if readiness_score < 50:
            confidence = "low"
        elif readiness_score < 70:
            confidence = "moderate"
        else:
            confidence = "high"

        # Performance level
        if pass_prob < 0.25:
            performance = "likely_fail"
            recommendation = "Significant additional study needed. Consider extending study period."
        elif pass_prob < 0.65:
            performance = "borderline"
            recommendation = "Continue focused study on weak topics. Practice exams recommended."
        elif pass_prob < 0.90:
            performance = "likely_pass"
            recommendation = "On track. Maintain current study pace and review weaker topics."
        else:
            performance = "very_likely_pass"
            recommendation = "Strong preparation. Focus on weak areas and take practice exams."

        return {
            'pass_probability': float(pass_prob),
            'confidence_level': confidence,
            'estimated_performance': performance,
            'recommendation': recommendation,
            'readiness_score': float(readiness_score),
        }

    def detect_weaknesses(
        self,
        topic_mastery: Dict[str, float],
        exam_weights: Dict[str, float],
        threshold: float = 0.5
    ) -> List[Dict]:
        """
        Identify topics below mastery threshold, prioritized by exam importance.

        Returns topics that need attention, sorted by:
        1. How far below threshold (gap)
        2. How important the topic is (weight)

        Args:
            topic_mastery: Dict mapping topic_id -> mastery (0-1).
            exam_weights: Dict mapping topic_id -> weight (typically 0-1 or 0-100).
            threshold: Mastery threshold below which topics are considered weak (default 0.5).

        Returns:
            List of weakness dicts, sorted by priority:
                - 'topic_id': str
                - 'mastery': float
                - 'weight': float
                - 'gap_below_threshold': float
                - 'priority': float (gap * weight)
        """
        weaknesses = []

        for topic_id, mastery in topic_mastery.items():
            if mastery < threshold:
                weight = exam_weights.get(topic_id, 1.0)
                gap = threshold - mastery
                priority = gap * weight

                weaknesses.append({
                    'topic_id': topic_id,
                    'mastery': float(mastery),
                    'weight': float(weight),
                    'gap_below_threshold': float(gap),
                    'priority': float(priority),
                })

        # Sort by priority (descending)
        weaknesses.sort(key=lambda x: x['priority'], reverse=True)

        return weaknesses

    def _wilson_confidence_interval(
        self,
        successes: int,
        trials: int,
        confidence: float = 0.95
    ) -> tuple:
        """
        Compute Wilson score confidence interval for binomial proportion.

        More accurate than simple normal approximation, especially for small samples.

        Args:
            successes: Number of successes (correct answers).
            trials: Total number of trials.
            confidence: Confidence level (default 0.95 for 95%).

        Returns:
            Tuple (lower_bound, upper_bound) for proportion confidence interval.
        """
        if trials == 0:
            return (0.0, 0.0)

        p = successes / trials
        z = 1.96  # 95% confidence level

        denominator = 1 + z * z / trials
        center = (p + z * z / (2 * trials)) / denominator
        margin = z * math.sqrt(p * (1 - p) / trials + z * z / (4 * trials * trials)) / denominator

        lower = max(0, center - margin)
        upper = min(1, center + margin)

        return (lower, upper)

    def get_learning_curve(
        self,
        performances: List[Dict],
        window_size: int = 10
    ) -> List[Dict]:
        """
        Compute smoothed learning curve showing accuracy over time.

        Uses moving average to smooth out noise.

        Args:
            performances: List of performance dicts with 'is_correct' key.
            window_size: Size of moving average window (default 10).

        Returns:
            List of learning curve points with:
                - 'question_number': int
                - 'rolling_accuracy': float
                - 'is_correct': bool
        """
        if not performances:
            return []

        curve = []
        window = []

        for idx, perf in enumerate(performances):
            is_correct = perf.get('is_correct', False)
            window.append(1 if is_correct else 0)

            if len(window) > window_size:
                window.pop(0)

            rolling_accuracy = sum(window) / len(window) if window else 0.0

            curve.append({
                'question_number': idx + 1,
                'rolling_accuracy': float(rolling_accuracy),
                'is_correct': is_correct,
            })

        return curve

    def estimate_time_to_readiness(
        self,
        current_readiness: float,
        target_readiness: float,
        hours_per_day: float,
        improvement_rate: float = 0.5  # points per day
    ) -> Dict:
        """
        Estimate time to reach target readiness score.

        Args:
            current_readiness: Current readiness score (0-100).
            target_readiness: Target readiness score (0-100).
            hours_per_day: Daily study hours available.
            improvement_rate: Expected improvement rate (points per day of study).

        Returns:
            Dict with:
                - 'days_needed': int
                - 'hours_needed': float
                - 'weeks_needed': float
                - 'is_achievable': bool (within 60 days)
        """
        if current_readiness >= target_readiness:
            return {
                'days_needed': 0,
                'hours_needed': 0.0,
                'weeks_needed': 0.0,
                'is_achievable': True,
            }

        gap = target_readiness - current_readiness
        # Scale improvement rate by study hours
        scaled_rate = improvement_rate * (hours_per_day / 2.0)

        days_needed = gap / scaled_rate if scaled_rate > 0 else 999
        hours_needed = days_needed * hours_per_day
        weeks_needed = days_needed / 7.0

        is_achievable = days_needed <= 60  # Assume 60-day study window

        return {
            'days_needed': int(math.ceil(days_needed)),
            'hours_needed': float(hours_needed),
            'weeks_needed': float(weeks_needed),
            'is_achievable': is_achievable,
        }
