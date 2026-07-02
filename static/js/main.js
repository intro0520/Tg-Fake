/**
 * 发卡系统管理后台 - 前端交互
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
            showAlert('商品添加成功！', 'success');
            setTimeout(() => location.reload(), 800);
        } else {
            showAlert('添加失败: ' + (result.detail || '未知错误'), 'danger');
        }
    } catch (error) {
        showAlert('网络错误', 'danger');
    }
}

async function deleteProduct(productId) {
    if (!confirm('确定要删除该商品？库存和订单也会被删除。')) return;
    try {
        const response = await fetch(`/api/products/${productId}`, { method: 'DELETE' });
        if (response.ok) {
            showAlert('删除成功！', 'success');
            setTimeout(() => location.reload(), 800);
        } else {
            showAlert('删除失败', 'danger');
        }
    } catch (error) {
        showAlert('网络错误', 'danger');
    }
}

// ==================== 库存管理 ====================

let currentProductId = null;

async function openStockModal(productId, productName) {
    currentProductId = productId;
    document.getElementById('stockModalTitle').textContent = "管理库存 - " + productName;
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
                    ${item.status === 1 ? '可用' : '已用'}
                </span>
            </div>
        `).join('');
    } catch (error) {
        document.getElementById('stockList').innerHTML = '<p class="text-muted">加载失败</p>';
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
        showAlert('请输入库存内容', 'warning');
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
            showAlert(`已添加 ${result.count} 条库存`, 'success');
            closeStockModal();
            setTimeout(() => location.reload(), 800);
        } else {
            showAlert('添加失败', 'danger');
        }
    } catch (error) {
        showAlert('网络错误', 'danger');
    }
}

async function clearStock() {
    if (!currentProductId) return;
    if (!confirm('确定要清空全部库存？此操作不可恢复！')) return;

    try {
        const response = await fetch(`/api/products/${currentProductId}/stock`, { method: 'DELETE' });
        if (response.ok) {
            showAlert('库存已清空', 'success');
            closeStockModal();
            setTimeout(() => location.reload(), 800);
        }
    } catch (error) {
        showAlert('网络错误', 'danger');
    }
}

// ==================== 订单操作 ====================

async function markPaid(orderId) {
    // 占位：Web 端标记支付
    showAlert('功能开发中...请在 Bot 端完成支付', 'warning');
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

    // 时间相对化
    document.querySelectorAll('.time-ago').forEach(el => {
        const ts = parseInt(el.dataset.timestamp) * 1000;
        const now = Date.now();
        const diff = now - ts;
        if (diff < 60000) el.textContent = '刚刚';
        else if (diff < 3600000) el.textContent = `${Math.floor(diff / 60000)} 分钟前`;
        else if (diff < 86400000) el.textContent = `${Math.floor(diff / 3600000)} 小时前`;
        else el.textContent = new Date(ts).toLocaleDateString();
    });
});
