from app.schemas.code import Base as CodeBase
from app.schemas.event import Base as EventBase
from app.schemas.favourite import Base as FavouriteBase
from app.schemas.order import Base as OrderBase
from app.schemas.organization import Base as OrganizationBase
from app.schemas.ticket import Base as TicketBase
from app.schemas.ticket_status_history import Base as TicketStatusHistoryBase
from app.schemas.user import Base as UserBase

Base = [CodeBase, UserBase, EventBase, FavouriteBase, OrderBase, OrganizationBase, TicketBase, TicketStatusHistoryBase]


