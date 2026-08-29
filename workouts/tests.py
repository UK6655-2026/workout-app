from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date
from workouts.models import Workout, Exercise, WorkoutSet, WeightRecord, Goal

class LoginTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )

    def test_login(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": "testuser",
                "password": "testpassword",
            }
        )

        self.assertRedirects(
            response,
            reverse("home")
        )

    def test_home_requires_login(self):
        response = self.client.get(
            reverse("home")
        )

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('home')}"
        )

    def test_home_after_login(self):
        self.client.login(
            username="testuser",
            password="testpassword"
        )

        response = self.client.get(
            reverse("home")
        )

        self.assertEqual(
            response.status_code,
            200
        )

class WorkoutTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="workoutuser",
            password="testpassword"
        )

        self.client.login(
            username="workoutuser",
            password="testpassword"
        )

    def test_workout_create(self):
        response = self.client.post(
            reverse("workout_list"),
            {
                "workout_date": date(2026, 8, 29),
                "memo": "胸トレ"
            }
        )

        self.assertRedirects(
            response,
            reverse("workout_list")
        )

        self.assertTrue(
            Workout.objects.filter(
                user=self.user,
                workout_date=date(2026, 8, 29),
                memo="胸トレ"
            ).exists()
        )

class ExerciseTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="exerciseuser",
            password="testpassword"
        )

        self.client.login(
            username="exerciseuser",
            password="testpassword"
        )

        self.workout = Workout.objects.create(
            user=self.user,
            workout_date=date(2026, 8, 29),
            memo="胸トレ"
        )

    def test_exercise_create(self):
        response = self.client.post(
            reverse(
                "exercise_create",
                args=[self.workout.id]
            ),
            {
                "name": "ベンチプレス"
            }
        )

        self.assertRedirects(
            response,
            reverse("workout_list")
        )

        self.assertTrue(
            Exercise.objects.filter(
                workout=self.workout,
                name="ベンチプレス"
            ).exists()
        )

class WorkoutSetTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="setuser",
            password="testpassword"
        )

        self.client.login(
            username="setuser",
            password="testpassword"
        )

        self.workout = Workout.objects.create(
            user=self.user,
            workout_date=date(2026, 8, 29),
            memo="胸トレ"
        )

        self.exercise = Exercise.objects.create(
            workout=self.workout,
            name="ベンチプレス"
        )

    def test_set_create(self):
        response = self.client.post(
            reverse(
                "set_create",
                args=[self.exercise.id]
            ),
            {
                "weight": "60.00",
                "reps": 10
            }
        )

        self.assertRedirects(
            response,
            reverse("workout_list")
        )

        self.assertTrue(
            WorkoutSet.objects.filter(
                exercise=self.exercise,
                weight="60.00",
                reps=10
            ).exists()
        )

class WorkoutSecurityTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1",
            password="testpassword"
        )

        self.user2 = User.objects.create_user(
            username="user2",
            password="testpassword"
        )

        self.workout = Workout.objects.create(
            user=self.user1,
            workout_date=date(2026, 8, 29),
            memo="user1のトレーニング"
        )

    def test_user_cannot_see_other_users_workout(self):
        self.client.login(
            username="user2",
            password="testpassword"
        )

        response = self.client.get(
            reverse("workout_list")
        )

        self.assertNotContains(
            response,
            "user1のトレーニング"
        )

class WorkoutEditTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="edituser",
            password="testpassword"
        )

        self.client.login(
            username="edituser",
            password="testpassword"
        )

        self.workout = Workout.objects.create(
            user=self.user,
            workout_date=date(2026, 8, 29),
            memo="編集前"
        )

    def test_workout_edit(self):
        response = self.client.post(
            reverse(
                "workout_edit",
                args=[self.workout.id]
            ),
            {
                "workout_date": date(2026, 8, 30),
                "memo": "編集後"
            }
        )

        self.assertRedirects(
            response,
            reverse("workout_list")
        )

        self.workout.refresh_from_db()

        self.assertEqual(
            self.workout.workout_date,
            date(2026, 8, 30)
        )

        self.assertEqual(
            self.workout.memo,
            "編集後"
        )

class WorkoutDeleteTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="deleteuser",
            password="testpassword"
        )

        self.client.login(
            username="deleteuser",
            password="testpassword"
        )

        self.workout = Workout.objects.create(
            user=self.user,
            workout_date=date(2026, 8, 29),
            memo="削除するトレーニング"
        )

    def test_workout_delete(self):
        response = self.client.post(
            reverse(
                "workout_delete",
                args=[self.workout.id]
            )
        )

        self.assertRedirects(
            response,
            reverse("workout_list")
        )

        self.assertFalse(
            Workout.objects.filter(
                id=self.workout.id
            ).exists()
        )

class WorkoutSecurityEditDeleteTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username="owner",
            password="testpassword"
        )

        self.user2 = User.objects.create_user(
            username="other",
            password="testpassword"
        )

        self.workout = Workout.objects.create(
            user=self.user1,
            workout_date=date(2026, 8, 29),
            memo="ownerのトレーニング"
        )

        self.client.login(
            username="other",
            password="testpassword"
        )

    def test_other_user_cannot_edit_workout(self):
        response = self.client.post(
            reverse(
                "workout_edit",
                args=[self.workout.id]
            ),
            {
                "workout_date": date(2026, 8, 30),
                "memo": "勝手に変更"
            }
        )

        self.assertEqual(
            response.status_code,
            404
        )

        self.workout.refresh_from_db()

        self.assertEqual(
            self.workout.memo,
            "ownerのトレーニング"
        )

    def test_other_user_cannot_delete_workout(self):
        response = self.client.post(
            reverse(
                "workout_delete",
                args=[self.workout.id]
            )
        )

        self.assertEqual(
            response.status_code,
            404
        )

        self.assertTrue(
            Workout.objects.filter(
                id=self.workout.id
            ).exists()
        )

class WeightRecordTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="weightuser",
            password="testpassword"
        )

        self.client.login(
            username="weightuser",
            password="testpassword"
        )

    def test_weight_create(self):
        response = self.client.post(
            reverse("weight_create"),
            {
                "date": date(2026, 8, 29),
                "weight": "70.50"
            }
        )

        self.assertRedirects(
            response,
            reverse("home")
        )

        self.assertTrue(
            WeightRecord.objects.filter(
                user=self.user,
                date=date(2026, 8, 29),
                weight="70.50"
            ).exists()
        )

    def test_weight_same_date_is_updated(self):
        WeightRecord.objects.create(
            user=self.user,
            date=date(2026, 8, 29),
            weight="70.00"
        )

        response = self.client.post(
            reverse("weight_create"),
            {
                "date": date(2026, 8, 29),
                "weight": "68.50"
            }
        )

        self.assertRedirects(
            response,
            reverse("home")
        )

        records = WeightRecord.objects.filter(
            user=self.user,
            date=date(2026, 8, 29)
        )

        self.assertEqual(
            records.count(),
            1
        )

        self.assertEqual(
            records.first().weight,
            68.50
        )

class WeightEditTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="weightedituser",
            password="testpassword"
        )

        self.client.login(
            username="weightedituser",
            password="testpassword"
        )

        self.weight = WeightRecord.objects.create(
            user=self.user,
            date=date(2026, 8, 29),
            weight="70.00"
        )

    def test_weight_edit(self):
        response = self.client.post(
            reverse(
                "weight_edit",
                args=[self.weight.id]
            ),
            {
                "date": date(2026, 8, 29),
                "weight": "68.50"
            }
        )

        self.assertRedirects(
            response,
            reverse("weight_list")
        )

        self.weight.refresh_from_db()

        self.assertEqual(
            self.weight.weight,
            68.50
        )

class WeightDeleteTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="weightdeleteuser",
            password="testpassword"
        )

        self.client.login(
            username="weightdeleteuser",
            password="testpassword"
        )

        self.weight = WeightRecord.objects.create(
            user=self.user,
            date=date(2026, 8, 29),
            weight="70.00"
        )

    def test_weight_delete(self):
        response = self.client.post(
            reverse(
                "weight_delete",
                args=[self.weight.id]
            )
        )

        self.assertRedirects(
            response,
            reverse("weight_list")
        )

        self.assertFalse(
            WeightRecord.objects.filter(
                id=self.weight.id
            ).exists()
        )

class WeightSecurityEditDeleteTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username="weightowner",
            password="testpassword"
        )

        self.user2 = User.objects.create_user(
            username="weightother",
            password="testpassword"
        )

        self.weight = WeightRecord.objects.create(
            user=self.user1,
            date=date(2026, 8, 29),
            weight="70.00"
        )

        self.client.login(
            username="weightother",
            password="testpassword"
        )

    def test_other_user_cannot_edit_weight(self):
        response = self.client.post(
            reverse(
                "weight_edit",
                args=[self.weight.id]
            ),
            {
                "date": date(2026, 8, 29),
                "weight": "60.00"
            }
        )

        self.assertEqual(
            response.status_code,
            404
        )

        self.weight.refresh_from_db()

        self.assertEqual(
            self.weight.weight,
            70.00
        )
    
    def test_other_user_cannot_delete_weight(self):
        response = self.client.post(
            reverse(
                "weight_delete",
                args=[self.weight.id]
            )
        )

        self.assertEqual(
            response.status_code,
            404
        )

        self.assertTrue(
            WeightRecord.objects.filter(
                id=self.weight.id
            ).exists()
        )

class GoalTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="goaluser",
            password="testpassword"
        )

        self.client.login(
            username="goaluser",
            password="testpassword"
        )

    def test_goal_create(self):
        response = self.client.post(
            reverse("goal_create"),
            {
                "future_goal": "ベンチプレス100kg",
                "one_month_goal": "ベンチプレス80kg"
            }
        )

        self.assertRedirects(
            response,
            reverse("home")
        )

        self.assertTrue(
            Goal.objects.filter(
                user=self.user,
                future_goal="ベンチプレス100kg",
                one_month_goal="ベンチプレス80kg"
            ).exists()
        )
    def test_goal_update(self):
        goal = Goal.objects.create(
            user=self.user,
            future_goal="ベンチプレス80kg",
            one_month_goal="ベンチプレス70kg"
        )

        response = self.client.post(
            reverse("goal_create"),
            {
                "future_goal": "ベンチプレス100kg",
                "one_month_goal": "ベンチプレス80kg"
            }
        )

        self.assertRedirects(
            response,
            reverse("home")
        )

        goal.refresh_from_db()

        self.assertEqual(
            goal.future_goal,
            "ベンチプレス100kg"
        )

        self.assertEqual(
            goal.one_month_goal,
            "ベンチプレス80kg"
        )

        self.assertEqual(
            Goal.objects.filter(
                user=self.user
            ).count(),
            1
        )
    def test_goal_is_separated_by_user(self):
        user2 = User.objects.create_user(
            username="goaluser2",
            password="testpassword"
        )

        Goal.objects.create(
            user=user2,
            future_goal="ユーザー2の目標",
            one_month_goal="ユーザー2の1ヶ月目標"
        )

        response = self.client.get(
            reverse("goal_create")
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertNotContains(
            response,
            "ユーザー2の目標"
        )

class StatisticsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="statisticsuser",
            password="testpassword"
        )

        self.client.login(
            username="statisticsuser",
            password="testpassword"
        )

    def test_statistics_counts(self):
        workout1 = Workout.objects.create(
            user=self.user,
            workout_date=date(2026, 8, 28),
            memo="胸トレ"
        )

        workout2 = Workout.objects.create(
            user=self.user,
            workout_date=date(2026, 8, 29),
            memo="背中トレ"
        )

        exercise1 = Exercise.objects.create(
            workout=workout1,
            name="ベンチプレス"
        )

        exercise2 = Exercise.objects.create(
            workout=workout1,
            name="ダンベルフライ"
        )

        exercise3 = Exercise.objects.create(
            workout=workout2,
            name="ラットプルダウン"
        )

        WorkoutSet.objects.create(
            exercise=exercise1,
            weight="60.00",
            reps=10
        )

        WorkoutSet.objects.create(
            exercise=exercise1,
            weight="65.00",
            reps=8
        )

        WorkoutSet.objects.create(
            exercise=exercise2,
            weight="20.00",
            reps=10
        )

        WorkoutSet.objects.create(
            exercise=exercise3,
            weight="50.00",
            reps=10
        )

        WorkoutSet.objects.create(
            exercise=exercise3,
            weight="55.00",
            reps=8
        )

        response = self.client.get(
            reverse("statistics")
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertEqual(
            response.context["workout_count"],
            2
        )

        self.assertEqual(
            response.context["exercise_count"],
            3
        )

        self.assertEqual(
            response.context["set_count"],
            5
        )
    
    def test_statistics_max_weight(self):
        workout = Workout.objects.create(
            user=self.user,
            workout_date=date(2026, 8, 29),
            memo="胸トレ"
        )

        exercise = Exercise.objects.create(
            workout=workout,
            name="ベンチプレス"
        )

        WorkoutSet.objects.create(
            exercise=exercise,
            weight="60.00",
            reps=10
        )

        WorkoutSet.objects.create(
            exercise=exercise,
            weight="70.00",
            reps=8
        )

        WorkoutSet.objects.create(
            exercise=exercise,
            weight="65.00",
            reps=8
        )

        response = self.client.get(
            reverse("statistics")
        )

        self.assertEqual(
            response.status_code,
            200
        )

        exercise_stats = response.context["exercise_stats"]

        self.assertEqual(
            len(exercise_stats),
            1
        )

        self.assertEqual(
            exercise_stats[0]["name"],
            "ベンチプレス"
        )

        self.assertEqual(
            exercise_stats[0]["max_weight"],
            70.0
        )
    
    def test_statistics_only_shows_current_user_data(self):
        other_user = User.objects.create_user(
            username="statisticsother",
            password="testpassword"
        )

        my_workout = Workout.objects.create(
            user=self.user,
            workout_date=date(2026, 8, 29),
            memo="自分のトレーニング"
        )

        my_exercise = Exercise.objects.create(
            workout=my_workout,
            name="ベンチプレス"
        )

        WorkoutSet.objects.create(
            exercise=my_exercise,
            weight="70.00",
            reps=10
        )

        other_workout = Workout.objects.create(
            user=other_user,
            workout_date=date(2026, 8, 29),
            memo="他ユーザーのトレーニング"
        )

        other_exercise = Exercise.objects.create(
            workout=other_workout,
            name="ベンチプレス"
        )

        WorkoutSet.objects.create(
            exercise=other_exercise,
            weight="150.00",
            reps=10
        )

        response = self.client.get(
            reverse("statistics")
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertEqual(
            response.context["workout_count"],
            1
        )

        self.assertEqual(
            response.context["exercise_count"],
            1
        )

        self.assertEqual(
            response.context["set_count"],
            1
        )

        exercise_stats = response.context["exercise_stats"]

        self.assertEqual(
            len(exercise_stats),
            1
        )

        self.assertEqual(
            exercise_stats[0]["max_weight"],
            70.0
        )
    
class CalendarTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="calendaruser",
            password="testpassword"
        )

        self.client.login(
            username="calendaruser",
            password="testpassword"
        )

    def test_workout_calendar_shows_training_dates(self):
        today = date.today()

        Workout.objects.create(
            user=self.user,
            workout_date=today,
            memo="今日のトレーニング"
        )

        response = self.client.get(
            reverse("workout_calendar")
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertIn(
            today.day,
            response.context["workout_dates"]
        )
    
    def test_workout_day_shows_workout(self):
        workout_date = date(2026, 8, 29)

        workout = Workout.objects.create(
            user=self.user,
            workout_date=workout_date,
            memo="胸トレをしました"
        )

        response = self.client.get(
            reverse(
                "workout_day",
                args=[
                    workout_date.year,
                    workout_date.month,
                    workout_date.day
                ]
            )
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertEqual(
            response.context["workout"],
            workout
        )
    
    def test_workout_day_cannot_show_other_user_workout(self):
        other_user = User.objects.create_user(
            username="calendarother",
            password="testpassword"
        )

        workout_date = date(2026, 8, 29)

        workout = Workout.objects.create(
            user=other_user,
            workout_date=workout_date,
            memo="他ユーザーのトレーニング"
        )

        response = self.client.get(
            reverse(
                "workout_day",
                args=[
                    workout_date.year,
                    workout_date.month,
                    workout_date.day
                ]
            )
        )

        self.assertEqual(
            response.status_code,
            404
        )

class LoginRequiredTest(TestCase):

    def test_workout_list_requires_login(self):
        response = self.client.get(
            reverse("workout_list")
        )

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('workout_list')}"
        )

    def test_weight_create_requires_login(self):
        response = self.client.get(
            reverse("weight_create")
        )

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('weight_create')}"
        )

    def test_goal_create_requires_login(self):
        response = self.client.get(
            reverse("goal_create")
        )

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('goal_create')}"
        )

    def test_statistics_requires_login(self):
        response = self.client.get(
            reverse("statistics")
        )

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('statistics')}"
        )

    def test_workout_calendar_requires_login(self):
        response = self.client.get(
            reverse("workout_calendar")
        )

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('workout_calendar')}"
        )