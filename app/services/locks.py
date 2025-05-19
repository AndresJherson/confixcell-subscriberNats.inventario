from datetime import datetime, timezone
from sqlmodel import Session, select

from app.entities import KardexLockEntity


async def intentar_bloquear_clave(session: Session, clave: str) -> bool:
    existe = session.exec(
        select(KardexLockEntity).where(KardexLockEntity.clave == clave)
    ).first()
    
    if existe:
        return False

    session.add(KardexLockEntity(
        clave=clave,
        fecha=datetime.now(timezone.utc)
    ))
    session.commit()
    return True


def liberar_clave(session: Session, clave: str):
    session.delete(
        select(KardexLockEntity).where(KardexLockEntity.clave == clave)
    )
    session.commit()
