from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for Task model with dependency handling
    """
    dependencies = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Task.objects.all(),
        required=False
    )
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'due_date', 'estimated_hours', 
                  'importance', 'dependencies', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_estimated_hours(self, value):
        """Validate estimated hours"""
        if value < 0.5:
            raise serializers.ValidationError(
                "Estimated hours must be at least 0.5"
            )
        return value

    def validate_importance(self, value):
        """Validate importance rating"""
        if value < 1 or value > 10:
            raise serializers.ValidationError(
                "Importance must be between 1 and 10"
            )
        return value


class TaskAnalysisInputSerializer(serializers.Serializer):
    """
    Serializer for task analysis input
    Accepts a list of tasks (can be existing or new)
    """
    tasks = serializers.ListField(
        child=serializers.DictField(),
        min_length=1,
        help_text="List of tasks to analyze"
    )
    strategy = serializers.ChoiceField(
        choices=['smart', 'fastest', 'impact', 'deadline'],
        default='smart',
        help_text="Sorting strategy to use"
    )

    def validate_tasks(self, value):
        """Validate task data in the list"""
        for idx, task_data in enumerate(value):
            # Check required fields
            required_fields = ['title', 'due_date', 'importance']
            for field in required_fields:
                if field not in task_data:
                    raise serializers.ValidationError(
                        f"Task at index {idx} is missing required field: {field}"
                    )
            
            # Validate importance
            importance = task_data.get('importance')
            if not isinstance(importance, int) or importance < 1 or importance > 10:
                raise serializers.ValidationError(
                    f"Task at index {idx} has invalid importance value. Must be 1-10"
                )
            
            # Set defaults for optional fields
            if 'estimated_hours' not in task_data:
                task_data['estimated_hours'] = 1
            
            if 'dependencies' not in task_data:
                task_data['dependencies'] = []
            
            # Validate estimated_hours
            estimated_hours = task_data.get('estimated_hours')
            if estimated_hours < 0.5:
                raise serializers.ValidationError(
                    f"Task at index {idx} has invalid estimated_hours. Must be at least 0.5"
                )
        
        return value


class TaskScoreSerializer(serializers.Serializer):
    """
    Serializer for task with calculated priority score
    """
    id = serializers.CharField()
    title = serializers.CharField()
    due_date = serializers.DateField()
    estimated_hours = serializers.FloatField()
    importance = serializers.IntegerField()
    dependencies = serializers.ListField(child=serializers.CharField())
    score = serializers.FloatField()
    priority_level = serializers.CharField()
    explanation = serializers.CharField()
    breakdown = serializers.DictField()


class TaskSuggestionSerializer(serializers.Serializer):
    """
    Serializer for task suggestions
    """
    task = TaskScoreSerializer()
    rank = serializers.IntegerField()
    recommendation = serializers.CharField()
