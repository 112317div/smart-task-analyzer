from django.test import TestCase
from .scoring import TaskPriorityScorer
from datetime import date, timedelta

class TaskScoringTests(TestCase):
    
    def test_urgency_overdue_task(self):
        """Test that overdue tasks get maximum urgency score"""
        scorer = TaskPriorityScorer()
        overdue_date = date.today() - timedelta(days=1)
        score, explanation = scorer.calculate_urgency_score(overdue_date)
        self.assertEqual(score, 40)
        self.assertIn("Overdue", explanation)
    
    def test_importance_high_score(self):
        """Test importance scoring for high-importance tasks"""
        scorer = TaskPriorityScorer()
        score, explanation = scorer.calculate_importance_score(9)
        self.assertGreater(score, 24)  # Should be > 80% of max
        self.assertIn("High importance", explanation)
    
    def test_effort_quick_win(self):
        """Test that tasks ≤1 hour are recognized as quick wins"""
        scorer = TaskPriorityScorer()
        score, explanation = scorer.calculate_effort_score(1.0)
        self.assertEqual(score, 15)  # Maximum effort score
        self.assertIn("Quick win", explanation)
    
    def test_circular_dependency_detection(self):
        """Test detection of circular dependencies"""
        scorer = TaskPriorityScorer()
        tasks = [
            {'id': '1', 'dependencies': ['2']},
            {'id': '2', 'dependencies': ['3']},
            {'id': '3', 'dependencies': ['1']}  # Circular!
        ]
        has_circular = scorer.detect_circular_dependencies(tasks)
        self.assertTrue(has_circular)
    
    def test_strategy_fastest_wins(self):
        """Test that 'fastest' strategy prioritizes low-effort tasks"""
        scorer = TaskPriorityScorer(strategy='fastest')
        self.assertEqual(scorer.multipliers['effort'], 4.0)
    
    def test_complete_priority_calculation(self):
        """Test complete priority calculation for a task"""
        scorer = TaskPriorityScorer()
        task = {
            'id': 'test_1',
            'title': 'Test Task',
            'due_date': (date.today() + timedelta(days=1)).strftime('%Y-%m-%d'),
            'estimated_hours': 2,
            'importance': 8,
            'dependencies': []
        }
        result = scorer.calculate_priority(task, [task])
        self.assertIn('score', result)
        self.assertIn('priority_level', result)
        self.assertGreater(result['score'], 0)
