/**
 * 发卡系统管理后台 - 前端交互
 * 支持双语：使用 window.gettext(key) 获取翻译
 */

// ==================== 商品操作 ====================

function toggleAddProductForm() {
    const card = document.getElementById('addProductCard');
    card.style.display = card.style.display === 'none' ? 'block' : 'none';
}

async function addProduct(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);

    try {
        const response = await fetch('/api/products', {
            method: 'POST',
            body: formData,
        });
        const result = await response.json();
        if (result.success) {
            showAlert(gettext('product_added'), 'success');
            setTimeout(() => location.reload(), 800);
        } else {
            showAlert(gettext('operation_failed') + ': ' + (result.detail || 'Unknown error'), 'danger');
        }
    } catch (error) {
        showAlert(gettext('network_error'), 'danger');
    }
}

async function deleteProduct(productId) {
    if (!confirm(gettext('confirm_delete_product'))) return;
    try {
        const response = await fetch(`/api/products/${productId}`, { method: 'DELETE' });
        if (response.ok) {
            showAlert(gettext('delete_success'), 'success');
            setTimeout(() => location.reload(), 800);
        } else {
            showAlert(gettext('delete_failed') || gettext('operation_failed'), 'danger');
        }
    } catch (error) {
        showAlert(gettext('network_error'), 'danger');
    }
}

// ==================== 库存管理 ====================

let currentProductId = null;

async function openStockModal(productId, productName) {
    currentProductId = productId;
    document.getElementById('stockModalTitle').textContent = gettext('manage_stock') + productName;
    document.getElementById('stockContents').value = '';
    document.getElementById('stockModal').classList.add('active');

    // 加载现有库存
    try {
        const response = await fetch(`/api/products/${productId}/stock`);
        const items = await response.json();
        const list = document.getElementById('stockList');
        list.innerHTML = items.map(item => `
            <div class="stock-item">
                ${escapeHtml(item.content)}
                <span class="badge badge-${item.status === 1 ? 'success' : 'secondary'}">
                    ${item.status === 1 ? gettext('available') : gettext('used')}
                </span>
            </div>
        `).join('');
    } catch (error) {
        document.getElementById('stockList').innerHTML = `<p class="text-muted">${gettext('load_failed')}</p>`;
    }
}

function closeStockModal() {
    document.getElementById('stockModal').classList.remove('active');
    currentProductId = null;
}

async function addStock() {
    if (!currentProductId) return;
    const contents = document.getElementById('stockContents').value;
    if (!contents.trim()) {
        showAlert(gettext('enter_stock_content'), 'warning');
        return;
    }

    try {
        const formData = new FormData();
        formData.append('contents', contents);
        const response = await fetch(`/api/products/${currentProductId}/stock`, {
            method: 'POST',
            body: formData,
        });
        const result = await response.json();
        if (result.success) {
            showAlert(gettext('stock_added').replace('{}', result.count), 'success');
            closeStockModal();
            setTimeout(() => location.reload(), 800);
        } else {
            showAlert(gettext('operation_failed'), 'danger');
        }
    } catch (error) {
        showAlert(gettext('network_error'), 'danger');
    }
}

async function clearStock() {
    if (!currentProductId) return;
    if (!confirm(gettext('confirm_clear_all'))) return;

    try {
        const response = await fetch(`/api/products/${currentProductId}/stock`, { method: 'DELETE' });
        if (response.ok) {
            showAlert(gettext('stock_cleared'), 'success');
            closeStockModal();
            setTimeout(() => location.reload(), 800);
        }
    } catch (error) {
        showAlert(gettext('network_error'), 'danger');
    }
}

// ==================== 订单操作 ====================

async function markPaid(orderId) {
    showAlert(gettext('feature_wip'), 'warning');
}

// ==================== 辅助函数 ====================

function showAlert(text, type = 'info') {
    const wrapper = document.querySelector('.content-wrapper');
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.innerHTML = `
        ${text}
        <button class="close" onclick="this.parentElement.remove()">×</button>
    `;
    wrapper.insertBefore(alert, wrapper.firstChild);
    setTimeout(() => alert.remove(), 5000);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// 侧边栏切换
document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.getElementById('sidebarToggle');
    if (toggle) {
        toggle.addEventListener('click', () => {
            document.getElementById('sidebar').classList.toggle('open');
        });
    }

    // 模态框外部点击关闭
    document.getElementById('stockModal')?.addEventListener('click', (e) => {
        if (e.target.id === 'stockModal') closeStockModal();
    });

    // ESC 关闭模态框
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeStockModal();
    });
});
