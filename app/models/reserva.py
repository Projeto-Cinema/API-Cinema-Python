
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import BaseModel

class Reserva(BaseModel):
    usuario_id = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    sessao_id = Column(Integer, ForeignKey("sessao.id"), nullable=False)
    codigo = Column(String(20), unique=True, nullable=False)
    data_reserva = Column(DateTime, nullable=False)
    status = Column(String(20), default="pendente", nullable=False)  # pendente, confirmada, cancelada, expirada
    valor_total = Column(Float, nullable=False)
    metodo_pagamento = Column(String(50), nullable=True)

    # Relacionamentos
    usuario = relationship("Usuario", back_populates="reservas")
    sessao = relationship("Sessao", back_populates="reservas")
    itens = relationship("ItemReserva", back_populates="reserva", cascade="all, delete-orphan")
    pagamento = relationship("Pagamento", back_populates="reserva", uselist=False)

    @property
    def reserve_seats(self):
        seats = []
        for item in self.itens:
            if item.tipo == "assento" and item.assento_sala:
                seats.append(item.assento_sala.codigo)

        return seats
    
    @property
    def reserved_products(self):
        products = []
        for item in self.itens:
            if item.tipo == "produto" and item.produto:
                products.append({
                    "nome": item.produto.nome,
                    "quantidade": item.quantidade,
                    "preco_unitario": item.preco_unitario,
                    "preco_total": item.preco_total})
        return products
    
    def add_seats(self, assento_sala_id: int, price: float):
        item = ItemReserva(
            reserva_id=self.id,
            item_id=assento_sala_id,
            tipo="assento",
            quantidade=1,
            preco_unitario=price,
            preco_total=price
        )
        self.itens.append(item)
        return item
    
    def add_product(self, product_id: int, quantity: int, unit_price: float, discount: float = 0):
        price_total = (unit_price * quantity) - discount
        item = ItemReserva(
            reserva_id=self.id,
            item_id=product_id,
            tipo="produto",
            quantidade=quantity,
            preco_unitario=unit_price,
            preco_total=price_total,
            desconto=discount
        )
        self.itens.append(item)
        return item
    
    def calculate_total_value(self):
        self.valor_total = sum(item.preco_total for item in self.itens)
        return self.valor_total
    
    def get_quantity_seats(self):
        return len([item for item in self.itens if item.tipo == "assento"])

    def __repr__(self):
        return f"<Reserva(codigo='{self.codigo}', usuario_id={self.usuario_id}, status='{self.status}')>"
    

class ItemReserva(BaseModel):
    __tablename__ = "item_reserva"

    reserva_id = Column(Integer, ForeignKey("reserva.id"), nullable=False)
    item_id = Column(Integer, nullable=False)
    tipo = Column(String(20), nullable=False)  # assento ou produto
    quantidade = Column(Integer, default=1, nullable=False)
    preco_unitario = Column(Float, nullable=False)
    preco_total = Column(Float, nullable=False)
    desconto = Column(Float, default=0, nullable=False)

    # Relacionamentos
    reserva = relationship("Reserva", back_populates="itens")
    
    assento_sala = relationship(
        "AssentoSala", 
        foreign_keys=[item_id], 
        primaryjoin="and_(ItemReserva.tipo == 'assento', ItemReserva.item_id==AssentoSala.id)", 
        viewonly=True
    )
    
    produto = relationship(
        "Produto", 
        foreign_keys=[item_id], 
        primaryjoin="and_(ItemReserva.tipo == 'produto', ItemReserva.item_id==Produto.id)", 
        viewonly=True
    )