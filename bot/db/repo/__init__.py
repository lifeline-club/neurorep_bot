from bot.db.repo.base_repo_module import BaseRepoModule


class UsersRepoModule(BaseRepoModule):
    def create_user_if_not_exists(self, user_id: int) -> None:
        request = f"SELECT * FROM users WHERE user_id = {user_id}"
        if not self.get_from_db(request):
            request = f"INSERT INTO users (user_id) VALUES ({user_id})"
            self.execute_command(request)

    def get_user_by_id(self, user_id: int) -> dict:
        request = f"SELECT * FROM users WHERE user_id = {user_id}"
        return self.get_from_db(request)[0]

    def get_user_state(self, user_id: int, showmeta: bool = False) -> dict:
        self.create_user_if_not_exists(user_id)
        user = self.get_user_by_id(user_id)
        if user:
            return {
                "state": user["state"],
                "meta": user["meta"] if showmeta else None,
            }

    def update_user_state(self, user_id: int, state: int, meta: str = "") -> None:
        self.create_user_if_not_exists(user_id)
        request = f"UPDATE users SET state = {state}, meta = '{meta}' WHERE user_id = {user_id}"
        self.execute_command(request)


class Repo:
    users: UsersRepoModule

    def __init__(self):
        self.users = UsersRepoModule
