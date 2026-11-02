import { getProductImage } from '../utils/productImages';
import { useConectado } from '../hooks/useConectado';

export default function CartSidebar({ cart, isOpen, onClose, onRemove, totalPrice, onCheckout }) {
    const conectado = useConectado();

    return (
        <>
            {/* Overlay oscuro */}
            <div
                className={`cart-overlay ${isOpen ? 'cart-overlay--visible' : ''}`}
                onClick={onClose}
            />

            {/* Panel lateral */}
            <aside className={`cart-sidebar ${isOpen ? 'cart-sidebar--open' : ''}`} id="cart-sidebar">
                <div className="cart-header">
                    <h2>🛒 Tu Carrito</h2>
                    <button className="cart-close-btn" onClick={onClose} id="cart-close-btn" aria-label="Cerrar carrito">✕</button>
                </div>

                <div className="cart-items">
                    {cart.length === 0 ? (
                        <p className="cart-empty">Tu carrito está vacío.</p>
                    ) : (
                        cart.map((item) => {
                            const imgSrc = getProductImage(item);
                            return (
                                <div key={item.id} className="cart-item">
                                    {imgSrc && (
                                        <img
                                            src={imgSrc}
                                            alt={item.nombre}
                                            className="cart-item-thumb"
                                            width="50"
                                            height="50"
                                            loading="lazy"
                                            decoding="async"
                                        />
                                    )}
                                    <div className="cart-item-info">
                                        <span className="cart-item-name">{item.nombre}</span>
                                        <span className="cart-item-qty">x{item.cantidad}</span>
                                    </div>
                                <div className="cart-item-right">
                                    <span className="cart-item-price">
                                        ${(item.precio_final * item.cantidad).toLocaleString('es-AR')}
                                    </span>
                                    <button
                                        className="cart-remove-btn"
                                        onClick={() => onRemove(item.id)}
                                        id={`cart-remove-${item.id}`}
                                        aria-label={`Eliminar ${item.nombre} del carrito`}
                                    >
                                        🗑️
                                    </button>
                                </div>
                            </div>
                            );
                        })
                    )}
                </div>

                {cart.length > 0 && (
                    <div className="cart-footer">
                        <div className="cart-total">
                            <span>Total:</span>
                            <strong>${totalPrice.toLocaleString('es-AR')}</strong>
                        </div>
                        {!conectado && (
                            <p
                                role="status"
                                style={{
                                    fontSize: '0.85rem',
                                    color: '#f59e0b',
                                    backgroundColor: 'rgba(245, 158, 11, 0.1)',
                                    padding: '0.6rem 0.8rem',
                                    borderRadius: '8px',
                                    marginBottom: '0.75rem',
                                    textAlign: 'center',
                                    border: '1px solid rgba(245, 158, 11, 0.25)',
                                }}
                            >
                                Podés mirar el catálogo, pero para comprar necesitás internet.
                            </p>
                        )}
                        <button
                            className="cart-checkout-btn"
                            id="cart-checkout-btn"
                            onClick={onCheckout}
                            disabled={!conectado}
                            style={!conectado ? { opacity: 0.5, cursor: 'not-allowed' } : {}}
                        >
                            Confirmar Compra
                        </button>
                    </div>
                )}
            </aside>
        </>
    );
}

