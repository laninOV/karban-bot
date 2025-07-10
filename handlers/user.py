from typing import Optional, List, Dict, Any

class User:
    """
    Класс пользователя для Telegram-бота Karban согласно техническому заданию.
    """

    def __init__(
        self,
        user_id: int,
        username: Optional[str] = None,
        first_name: Optional[str] = None,
        registered: bool = False,
        krb: int = 0,
        rep: int = 0,
        archetype: Optional[str] = None,
        diary: str = "",
        referrals: Optional[List[int]] = None,
        influence: int = 0,
        wallet_history: Optional[List[Dict[str, Any]]] = None,
        referral_link: Optional[str] = None,
        role: Optional[str] = None,
    ):
        self.user_id = user_id
        self.username = username
        self.first_name = first_name
        self.registered = registered
        self.krb = krb  # Баланс KRB
        self.rep = rep  # Репутация
        self.archetype = archetype  # Архетип (Резидент/Юн)
        self.diary = diary  # Записи дневника
        self.referrals = referrals if referrals is not None else []  # ID приглашённых
        self.influence = influence  # Шкала влияния (геймификация)
        self.wallet_history = wallet_history if wallet_history is not None else []  # История операций
        self.referral_link = referral_link  # Персональная реферальная ссылка
        self.role = role  # Роль (например, "Резидент" или "Юн")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.user_id,
            "username": self.username,
            "first_name": self.first_name,
            "registered": self.registered,
            "krb": self.krb,
            "rep": self.rep,
            "archetype": self.archetype,
            "diary": self.diary,
            "referrals": self.referrals,
            "influence": self.influence,
            "wallet_history": self.wallet_history,
            "referral_link": self.referral_link,
            "role": self.role,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "User":
        return cls(
            user_id=data.get("id"),
            username=data.get("username"),
            first_name=data.get("first_name"),
            registered=data.get("registered", False),
            krb=data.get("krb", 0),
            rep=data.get("rep", 0),
            archetype=data.get("archetype"),
            diary=data.get("diary", ""),
            referrals=data.get("referrals", []),
            influence=data.get("influence", 0),
            wallet_history=data.get("wallet_history", []),
            referral_link=data.get("referral_link"),
            role=data.get("role"),
        )

    def add_krb(self, amount: int, reason: str = ""):
        self.krb += amount
        self.wallet_history.append({
            "type": "KRB",
            "amount": amount,
            "reason": reason
        })

    def add_rep(self, amount: int, reason: str = ""):
        self.rep += amount
        self.wallet_history.append({
            "type": "REP",
            "amount": amount,
            "reason": reason
        })

    def add_referral(self, referral_id: int):
        if referral_id not in self.referrals:
            self.referrals.append(referral_id)
            self.influence += 1

    def set_diary(self, text: str):
        self.diary = text

    def set_archetype(self, archetype: str):
        self.archetype = archetype

    def set_role(self, role: str):
        self.role = role

    def set_referral_link(self, link: str):
        self.referral_link = link

    def __str__(self):
        return (
            f"User({self.user_id}, {self.username}, {self.first_name}, "
            f"registered={self.registered}, krb={self.krb}, rep={self.rep}, "
            f"archetype={self.archetype}, influence={self.influence}, role={self.role})"
        )
