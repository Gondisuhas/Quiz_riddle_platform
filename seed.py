"""Seed script: creates the admin user, a demo player, sample quizzes and riddles.

Run:  python seed.py
Logins created:
  Admin   -> admin@quiz.local / admin123
  Player  -> alice@quiz.local  / alice123
"""
from app import create_app
from app.extensions import db
from app.models import User, Quiz, Question, Riddle

app = create_app()

with app.app_context():
    admin = User.query.filter_by(email="admin@quiz.local").first()
    if admin is None:
        admin = User(name="Admin", email="admin@quiz.local", role="admin")
        admin.set_password("admin123")
        db.session.add(admin)

    alice = User.query.filter_by(email="alice@quiz.local").first()
    if alice is None:
        alice = User(name="Alice", email="alice@quiz.local", role="user")
        alice.set_password("alice123")
        db.session.add(alice)

    db.session.commit()

    if Quiz.query.count() == 0:
        gk = Quiz(
            title="General Knowledge",
            description="Quick-fire trivia to warm up.",
            category="Trivia",
            difficulty="easy",
        )
        db.session.add(gk)
        db.session.flush()
        db.session.add_all(
            [
                Question(
                    quiz_id=gk.id,
                    question_text="What is the capital of France?",
                    option_a="Berlin", option_b="Madrid", option_c="Paris", option_d="Rome",
                    correct_answer="C", difficulty="easy",
                ),
                Question(
                    quiz_id=gk.id,
                    question_text="How many continents are there?",
                    option_a="5", option_b="6", option_c="7", option_d="8",
                    correct_answer="C", difficulty="easy",
                ),
                Question(
                    quiz_id=gk.id,
                    question_text="Which planet is known as the Red Planet?",
                    option_a="Venus", option_b="Mars", option_c="Jupiter", option_d="Saturn",
                    correct_answer="B", difficulty="easy",
                ),
            ]
        )

        sci = Quiz(
            title="Science Basics",
            description="Fundamentals of science.",
            category="Science",
            difficulty="medium",
        )
        db.session.add(sci)
        db.session.flush()
        db.session.add_all(
            [
                Question(
                    quiz_id=sci.id,
                    question_text="What is H2O commonly known as?",
                    option_a="Salt", option_b="Hydrogen peroxide", option_c="Water", option_d="Ammonia",
                    correct_answer="C", difficulty="easy",
                ),
                Question(
                    quiz_id=sci.id,
                    question_text="What force keeps us on the ground?",
                    option_a="Magnetism", option_b="Friction", option_c="Gravity", option_d="Tension",
                    correct_answer="C", difficulty="easy",
                ),
            ]
        )
        db.session.commit()
        print("Seeded 2 quizzes with 5 questions.")

    if Riddle.query.count() == 0:
        db.session.add_all(
            [
                Riddle(
                    riddle_text="The more you take, the more you leave behind. What am I?",
                    answer="footsteps", difficulty="medium",
                ),
                Riddle(
                    riddle_text="I have hands but cannot clap. What am I?",
                    answer="a clock", difficulty="easy",
                ),
                Riddle(
                    riddle_text="What has a head and a tail but no body?",
                    answer="a coin", difficulty="medium",
                ),
            ]
        )
        db.session.commit()
        print("Seeded 3 riddles.")

    print("Seed complete.")
    print("  Admin login -> admin@quiz.local / admin123")
    print("  Player login -> alice@quiz.local / alice123")
