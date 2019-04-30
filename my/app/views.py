"""Kaboom views."""
import random
from psycopg2.extensions import TransactionRollbackError
from sqlalchemy.exc import OperationalError
from websauna.system.http import Request
from websauna.system.core.route import simple_route
from websauna.system.core.redis import get_redis
from .models import MyModel


RETRY_ATTEMPT_KEY = 'tmp_attempt_count'


@simple_route("/", route_name="home", renderer='my.app/home.html')
def home(request: Request):
    return {"project": "Kaboom".format(count)}


# These functions using redis don't work as intended with multiple threads or concurrent users,
# but for demo purposes with a single user they should be ok

def get_retry_attempt_count(request):
    redis = get_redis(request)
    return int(redis.get(RETRY_ATTEMPT_KEY) or 0)


def increment_retry_attempt_count(request):
    redis = get_redis(request)
    if redis.get(RETRY_ATTEMPT_KEY) is None:
        redis.set(RETRY_ATTEMPT_KEY, 1, ex=2)
    else:
        redis.incr(RETRY_ATTEMPT_KEY)


def reset_retry_attempt_count(request):
    redis = get_redis(request)
    redis.delete(RETRY_ATTEMPT_KEY)


def simulate_possible_serialization_error(request, success_chance_one_in_n):
    # We need to open the DBSession. Any query will do
    count = request.dbsession.query(MyModel).count()
    # Roll the dice and throw a serialization error if we got unlucky
    dice_roll = random.randint(0, success_chance_one_in_n - 1)
    if dice_roll:
        print("\n\tSERIALIZATION ERROR, ATTEMPT #{}\n".format(get_retry_attempt_count(request)))
        raise OperationalError(
            statement="SELECT herpaderp",
            params=[],
            orig=TransactionRollbackError("""\
could not serialize access due to read/write dependencies among transactions
DETAIL:  Reason code: Canceled on identification as a pivot, during write.
HINT:  The transaction might succeed if retried.
            """)
        )


@simple_route("/kaboom", route_name="kaboom", renderer='my.app/kaboom.html')
def kaboom(request: Request):
    print("Kaboom! tx:", request.tm.get(), 'request:', id(request))
    increment_retry_attempt_count(request)
    attempt = get_retry_attempt_count(request)
    success_chance_one_in_n = 5
    simulate_possible_serialization_error(request, success_chance_one_in_n)
    reset_retry_attempt_count(request)  # No error, we can reset here
    return {"attempt": attempt, "chance": "1 / {}".format(success_chance_one_in_n) }
