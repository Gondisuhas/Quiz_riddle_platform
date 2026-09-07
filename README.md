# Quiz & Riddle Competition Platform — Backend

Member A deliverable (backend & integration) for the team workflow. Flask + Flask-SocketIO
REST API with SQLite, session auth, progressive quiz unlocks, automatic scoring and a
Socket.IO live leaderboard.

## Tech stack

- **Backend:** Flask + Flask-SocketIO (threaded async mode for dev)
- **Database:** SQLite via SQLAlchemy
- **Auth:** Flask-Login (session-based, hashed passwords)
- **Tests:** pytest (37 tests)

## Quick start

```bash
cd backend
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python seed.py          # admin + demo player + sample quizzes/riddles
python run.py           # http://127.0.0.1:5000
```

Default logins: **admin@quiz.local / admin123** · **alice@quiz.local / alice123**

## Run tests

```bash
pytest -q
```

## Endpoint map

### Auth — `/api/auth`
| Method | Path | Description |
|---|---|---|
| POST | `/api/auth/register` | Register (role `user`), auto-login |
| POST | `/api/auth/login` | Login, sets session cookie |
| POST | `/api/auth/logout` | Logout |
| GET | `/api/auth/me` | Current user |

### User portal — `/api`
| Method | Path | Description |
|---|---|---|
| GET | `/api/quizzes` | Quizzes with progressive-unlock state |
| GET | `/api/quizzes/<id>` | Quiz detail incl. unlocked questions |
| POST | `/api/quizzes/<id>/answer` | Submit answer, score, unlock next |
| GET | `/api/riddles` | Riddles with solved state |
| POST | `/api/riddles/<id>/answer` | Submit riddle answer (retry allowed) |
| GET | `/api/scores` | My scores / history |
| GET | `/api/leaderboard` | Overall leaderboard |

### Admin — `/api/admin` (role: admin)
| Method | Path | Description |
|---|---|---|
| GET | `/api/admin/stats` | Users/quizzes/questions/riddles/submissions/scores |
| GET/POST | `/api/admin/users` | List / create users |
| PUT/DELETE | `/api/admin/users/<id>` | Update / delete user |
| GET/POST | `/api/admin/quizzes` | List (with answers) / create quiz |
| PUT/DELETE | `/api/admin/quizzes/<id>` | Update / delete quiz |
| GET/POST | `/api/admin/quizzes/<id>/questions` | List / create question |
| PUT/DELETE | `/api/admin/questions/<id>` | Update / delete question |
| GET/POST | `/api/admin/riddles` | List (with answers) / create riddle |
| PUT/DELETE | `/api/admin/riddles/<id>` | Update / delete riddle |

## Realtime

Socket.IO event `leaderboard_update` (`{quiz_id, leaderboard}`) is emitted whenever a
correct answer is scored — quiz-scoped leaderboard for quiz answers, overall leaderboard
for riddle solves. Messages are structured for cross-language clients.

## Project layout

```
app/
  __init__.py       app factory
  config.py         configuration
  extensions.py     db, login_manager, socketio
  models.py         User, Quiz, Question, Riddle, Score, Submission
  api/
    __init__.py     root blueprint, admin_required + error helpers
    auth.py         register / login / logout / me
    participant.py  quizzes, riddles, answers, scores, leaderboard
    admin.py        users/quizzes/questions/riddles CRUD + stats
  scoring/
    engine.py       evaluate(), grade_riddle() (integration seam)
  realtime/
    events.py       broadcast_leaderboard(), Socket.IO handlers
tests/              pytest suite
run.py              entry point
seed.py             admin + demo player + sample data
requirements.txt
```

## Project structure (models)

- `users` 1→N `scores`, 1→N `submissions`
- `quizzes` 1→N `questions` (CASCADE)
- `scores` references `quiz_id` or `riddle_id` (both nullable)
- `riddles` independent content

## Assumptions

- Unknown "team unlock" semantics → implemented as **progressive unlock**: question *n+1*
  unlocks after question *n* is answered; the first question is always free.
- Submission rule: **one attempt per question** (later tries score 0 and are flagged
  `already_answered`); wrong riddle answers may be retried, points only on first success.
- Scoring: easy 1 pt, medium 2 pt, hard 3 pt.
- Auth is **session-based** (Flask-Login); send the session cookie on every request.
- CORS open (`*`) for local dev so the admin/user portals can connect from another origin.
