import streamlit as st
import math
import os
import sys

# --- 新增：解决打包后资源路径问题 ---
def resource_path(relative_path):
    """ 获取资源的绝对路径，用于 PyInstaller 打包 """
    try:
        base_path = sys._MEIPASS  # PyInstaller 临时文件夹
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
# -----------------------------------

def calculate_required_5_star_reviews(n_list, target_score):
    if len(n_list) != 5:
        raise ValueError("n_list 应包含 5 个元素，依次代表 1-5 星评价数量")

    total_reviews = sum(n_list)
    if total_reviews == 0:
        raise ValueError("总评价数为0，无法计算评分")

    current_total_score = sum((i + 1) * n for i, n in enumerate(n_list))
    current_score = current_total_score / total_reviews

    if target_score <= current_score:
        return 0, current_score

    numerator = target_score * total_reviews - current_total_score
    denominator = 5 - target_score

    if denominator <= 0:
        raise ValueError("目标评分必须小于 5 且高于当前评分")

    required_5_star = numerator / denominator
    required_5_star = math.ceil(required_5_star)
    return required_5_star, current_score


# Streamlit 界面
st.title("📊 酒店评分提升计算器")
st.markdown("请输入当前各星级评价数量：")

col1, col2, col3, col4, col5 = st.columns(5)
n1 = col1.number_input("1星评价", min_value=0, value=10)
n2 = col2.number_input("2星评价", min_value=0, value=10)
n3 = col3.number_input("3星评价", min_value=0, value=30)
n4 = col4.number_input("4星评价", min_value=0, value=150)
n5 = col5.number_input("5星评价", min_value=0, value=800)

n_list = [n1, n2, n3, n4, n5]
target_score = st.slider("🎯 目标评分（4.65 ~ 5.0）", min_value=4.65, max_value=5.0, value=4.8, step=0.01)

try:
    required_5_star, current_score = calculate_required_5_star_reviews(n_list, target_score)
    st.success(f"✅ 当前评分为：**{current_score:.3f} 分**")

    if required_5_star == 0:
        st.info(f"🎉 当前评分已达到目标评分 {target_score:.2f} 分，无需新增好评！")
    else:
        st.info(f"📈 将评分提升到 {target_score:.2f} 分，还需要大约 **{required_5_star}** 条 5星好评")
except ValueError as e:
    st.error(f"❌ 错误：{str(e)}")


# --- 新增：防止窗口立即关闭（可选）---
if __name__ == "__main__":
    pass