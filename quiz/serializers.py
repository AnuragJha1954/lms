from rest_framework import serializers
from quiz.models import Quiz, Question, Option, Answer, QuestionResponse, QuizAttempt
from users.models import CustomUser
from v1.models import Topic


class OptionCreateSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=255)


class QuestionCreateSerializer(serializers.Serializer):
    text = serializers.CharField()
    marks = serializers.FloatField(default=1.0)
    is_multiple_choice = serializers.BooleanField(default=False)
    options = OptionCreateSerializer(many=True)
    correct_option_indexes = serializers.ListField(
        child=serializers.IntegerField(min_value=0), allow_empty=False,
        help_text="Index(es) of correct options from the options list (starting at 0)"
    )


class QuizCreateSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField(allow_blank=True, required=False)
    quiz_type = serializers.ChoiceField(choices=[('topic', 'Topic Quiz'), ('teacher', 'Teacher Quiz')])
    questions = QuestionCreateSerializer(many=True)

    def validate(self, data):
        quiz_type = data.get('quiz_type')
        if quiz_type == 'teacher' and not self.context.get('teacher'):
            raise serializers.ValidationError("Teacher ID is required for Teacher Quiz.")
        return data

    def create(self, validated_data):
        topic = self.context['topic']
        teacher = self.context.get('teacher')
        quiz_type = validated_data['quiz_type']

        quiz = Quiz.objects.create(
            title=validated_data['title'],
            description=validated_data.get('description'),
            quiz_type=quiz_type,
            topic=topic,
            teacher=teacher if quiz_type == 'teacher' else None
        )

        for q_data in validated_data['questions']:
            question = Question.objects.create(
                quiz=quiz,
                text=q_data['text'],
                marks=q_data.get('marks', 1.0),
                is_multiple_choice=q_data.get('is_multiple_choice', False)
            )

            option_objs = []
            for option_data in q_data['options']:
                option = Option.objects.create(question=question, text=option_data['text'])
                option_objs.append(option)

            for idx in q_data['correct_option_indexes']:
                if idx < 0 or idx >= len(option_objs):
                    raise serializers.ValidationError(f"Invalid correct option index: {idx}")
                Answer.objects.create(question=question, option=option_objs[idx])

        return quiz






class StudentAnswerSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    selected_option_ids = serializers.ListField(
        child=serializers.IntegerField(), allow_empty=False
    )


class QuizAttemptSerializer(serializers.Serializer):
    quiz_id = serializers.IntegerField()
    answers = StudentAnswerSerializer(many=True)

    def validate(self, data):
        quiz_id = data['quiz_id']
        answers = data['answers']
        try:
            self.quiz = Quiz.objects.get(id=quiz_id)
        except Quiz.DoesNotExist:
            raise serializers.ValidationError("Quiz not found.")

        question_ids = self.quiz.questions.values_list('id', flat=True)
        for ans in answers:
            if ans['question_id'] not in question_ids:
                raise serializers.ValidationError(f"Question {ans['question_id']} does not belong to this quiz.")
        return data

    def create(self, validated_data):
        student = self.context['student']
        quiz = self.quiz
        answers_data = validated_data['answers']

        if QuizAttempt.objects.filter(student=student, quiz=quiz).exists():
            raise serializers.ValidationError("You have already attempted this quiz.")

        attempt = QuizAttempt.objects.create(student=student, quiz=quiz, is_submitted=True)

        total_score = 0

        for ans_data in answers_data:
            question = Question.objects.get(id=ans_data['question_id'])
            selected_options = Option.objects.filter(id__in=ans_data['selected_option_ids'], question=question)

            response = QuestionResponse.objects.create(
                attempt=attempt,
                question=question
            )
            response.selected_options.set(selected_options)

            correct_options = question.answers.values_list('option_id', flat=True)
            selected_option_ids = set(selected_options.values_list('id', flat=True))

            if set(correct_options) == selected_option_ids:
                response.is_correct = True
                total_score += question.marks

            response.save()

        attempt.score = total_score
        attempt.completed_at = attempt.started_at
        attempt.save()

        return attempt
    
    







class QuizListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'quiz_type', 'created_at', 'is_active']







class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text']

class QuestionWithOptionsSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'marks', 'is_multiple_choice', 'options']

class QuizDetailWithQuestionsSerializer(serializers.ModelSerializer):
    questions = QuestionWithOptionsSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'quiz_type', 'created_at', 'is_active', 'questions']


