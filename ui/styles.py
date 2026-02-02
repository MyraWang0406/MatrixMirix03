"""全局样式：蓝色主题、隐藏工具栏、电梯导航、决策结论、响应式"""


def get_global_styles() -> str:
    return """
<style>
/* ===== 隐藏 Streamlit 工具条 / Deploy 干扰 ===== */
[data-testid="stToolbar"], [data-testid="stAppToolbar"],
[data-testid="stDeployButton"], [data-testid="stHeaderToolbar"],
header[data-testid="stHeader"], .stDeployButton,
[kind="header"] { display: none !important; }
/* 兜底选择器 */
div[data-testid="stToolbar"] { display: none !important; }

/* ===== 去除顶部空白 ===== */
.main .block-container { padding-top: 0.5rem !important; padding-bottom: 2rem !important; }
.stApp > header { padding-top: 0 !important; }
/* 标题区紧贴上方 */
#main-header { margin-top: -0.5rem !important; }

/* ===== 标题区：深浅蓝渐变 + 水波 ===== */
.title-banner {
    background: linear-gradient(135deg, #1e3a5f 0%, #2d5a87 25%, #3d7ab5 50%, #2d5a87 75%, #1e3a5f 100%);
    background-size: 200% 200%;
    animation: wave 8s ease infinite;
    padding: 0.75rem 1.2rem;
    margin: -0.5rem -1rem 0.8rem -1rem;
    border-radius: 0 0 10px 10px;
}
@keyframes wave {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}
.title-banner h1, .title-banner .title-text { color: #fff !important; margin: 0 !important; font-weight: 600; font-size: 1.1rem; }

/* ===== 联系作者：右下角黑底白字 ===== */
.contact-footer {
    position: fixed; bottom: 0; right: 0;
    background: #1a1a1a; color: #fff;
    padding: 0.35rem 0.7rem; font-size: 0.8rem;
    border-radius: 8px 0 0 0; z-index: 999;
}
.contact-footer a { color: #fff; text-decoration: none; }

/* ===== 电梯导航 ===== */
.elevator-title { font-weight: 600; margin-bottom: 0.4rem; font-size: 0.95rem; }
.elevator-link { display: block; padding: 0.35rem 0.5rem; margin: 0.15rem 0; border-radius: 6px; font-size: 0.85rem; color: #334155; text-decoration: none; }
.elevator-link:hover { background: #e2e8f0; }
.elevator-link.active { background: #2563eb; color: #fff !important; }
.nav-pill { padding: 0.3rem 0.6rem; margin: 0.2rem 0; border-radius: 6px; font-size: 0.9rem; }
.nav-pill:hover { background: #e8f4fc; }

/* ===== 决策结论 Summary ===== */
.decision-summary-hero { padding: 1rem 1.2rem; margin: 1rem 0; border-radius: 8px; border-left: 4px solid #94a3b8; }
.decision-summary-hero.status-pass { background: #f0fdf4; border-left-color: #22c55e; }
.decision-summary-hero.status-fail { background: #fef2f2; border-left-color: #ef4444; }
.decision-summary-hero.status-warn { background: #fffbeb; border-left-color: #f59e0b; }
.summary-label { font-weight: 600; margin-bottom: 0.5rem; }
.summary-status { font-size: 1.15rem; font-weight: 600; margin: 0.5rem 0; }
.summary-row { margin: 0.3rem 0; font-size: 0.95rem; }

/* ===== 表格单层横向滚动 ===== */
[data-testid="stDataFrame"], .stDataFrame { overflow-x: auto !important; max-width: 100%; }
[data-testid="stDataFrame"] > div { overflow-x: auto !important; }
.stDataFrameResizer { overflow-x: auto !important; }

/* ===== 主色蓝色 ===== */
button[kind="primary"] { background-color: #2563eb !important; }
[data-testid="stMetric"] { font-size: 1rem !important; }
[data-testid="stMetric"] label { font-size: 0.85rem !important; }
.title-banner { position: sticky !important; top: 0 !important; z-index: 100 !important; }

/* ===== 元素卡片 ===== */
.elem-card { border: 1px solid #e2e8f0; border-radius: 8px; padding: 0.6rem 0.8rem; margin: 0.4rem 0; cursor: pointer; background: #fafafa; }
.elem-card:hover { background: #f1f5f9; border-color: #94a3b8; }
.elem-card.active { border-color: #2563eb; background: #eff6ff; }

/* ===== 布局统一与修复重叠 ===== */
.stSelectbox > div, .stMultiSelect > div { min-height: 2.5rem !important; }
/* 修复多选框标签过长导致的重叠 */
[data-testid="stMultiSelect"] span[data-baseweb="tag"] {
    max-width: 150px !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    white-space: nowrap !important;
}
/* 调整容器间距 */
[data-testid="stVerticalBlock"] > div {
    padding-top: 0.1rem !important;
    padding-bottom: 0.1rem !important;
}
/* 响应式调整 */
@media (max-width: 768px) {
    .main .block-container { padding: 0.5rem !important; max-width: 100% !important; }
}
</style>
"""
