from monitox.models import Session, UserRole, Users


def process_start(user_id: int) -> None:
    with Session() as session:
        user = session.query(Users).filter_by(user_id=user_id).first()

        if not user:
            new_user = Users(user_id=user_id, role=UserRole.ROLE_USER)
            session.add(new_user)
            session.commit()
