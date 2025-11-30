from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


class Task(models.Model):
    """
    Task model for storing task information.
    Each task can have dependencies on other tasks.
    """
    title = models.CharField(max_length=200)
    due_date = models.DateField()
    estimated_hours = models.FloatField(
        validators=[MinValueValidator(0.5)],
        help_text="Estimated hours to complete the task"
    )
    importance = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Importance rating from 1 (low) to 10 (high)"
    )
    dependencies = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='dependent_tasks',
        blank=True,
        help_text="Tasks that must be completed before this task"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def __str__(self):
        return f"{self.title} (Due: {self.due_date})"

    def clean(self):
        """Validate task data"""
        super().clean()
        
        if self.estimated_hours is not None and self.estimated_hours < 0.5:
            raise ValidationError({
                'estimated_hours': 'Estimated hours must be at least 0.5'
            })
        
        if self.importance is not None and (self.importance < 1 or self.importance > 10):
            raise ValidationError({
                'importance': 'Importance must be between 1 and 10'
            })

    def get_blocking_tasks(self):
        """Get all tasks that depend on this task"""
        return self.dependent_tasks.all()

    def get_dependency_count(self):
        """Count how many tasks depend on this task"""
        return self.dependent_tasks.count()

    def to_dict(self):
        """Convert task to dictionary representation"""
        return {
            'id': self.id,
            'title': self.title,
            'due_date': self.due_date.isoformat(),
            'estimated_hours': float(self.estimated_hours),
            'importance': self.importance,
            'dependencies': list(self.dependencies.values_list('id', flat=True))
        }