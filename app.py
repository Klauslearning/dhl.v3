import streamlit as st
import pandas as pd
import os
from utils import local_lookup, query_uk_tariff_api, append_sku_record

def format_commodity_code(code):
    digits = ''.join(filter(str.isdigit, str(code)))
    if len(digits) == 8:
        return f"{digits[:4]}.{digits[4:6]}.{digits[6:]}"
    return str(code)

# App title
st.set_page_config(page_title="DHL 发货自动生成系统 v4", layout="wide")
st.title("📦 DHL 发货自动生成系统 v4")

# Step 1: 上传订单文件
uploaded_file = st.file_uploader("上传订单文件 (CSV/Excel)", type=["csv", "xlsx", "xls"])

if uploaded_file:
    # Step 2: 只提取两列
    if uploaded_file.name.endswith("csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    
    # 只保留 Item Description 和 Selling Price
    col_map = {c.lower().strip(): c for c in df.columns}
    desc_col = col_map.get("item description")
    price_col = col_map.get("selling price")
    if not desc_col or not price_col:
        st.error("请确保文件包含 'Item Description' 和 'Selling Price' 两列！")
        st.stop()
    df = df[[desc_col, price_col]].copy()
    df.columns = ["Item Description", "Selling Price"]

    # Step 2: 数据预处理
    results = []
    for _, row in df.iterrows():
        desc = str(row["Item Description"]).strip()
        price = row["Selling Price"]
        local = local_lookup(desc)
        code = local["Commodity Code"] if local and local["Commodity Code"] else ""
        weight = local["Weight"] if local and local["Weight"] else ""
        origin = local["Origin Country"] if local and local["Origin Country"] else ""
        # 若找不到 commodity code，调用 API
        if not code and desc:
            code = query_uk_tariff_api(desc)
        results.append({
            "Item Description": desc,
            "Selling Price": price,
            "Weight": weight,
            "Origin Country": origin,
            "Commodity Code": code,
            "写入 SKU 数据库": False
        })
    edit_df = pd.DataFrame(results)

    st.subheader("📝 可编辑商品信息表")
    st.info("请补全缺失字段，勾选需要写入 SKU 数据库的行")
    edited = st.data_editor(
        edit_df,
        use_container_width=True,
        num_rows="dynamic",
        column_config={
            "写入 SKU 数据库": st.column_config.CheckboxColumn(
                "写入 SKU 数据库",
                help="勾选后，所有字段不为空时会写入 sku_reference_data.csv"
            )
        }
    )

    # Step 4: 提交后处理逻辑
    if st.button("提交并导出 DHL 文件"):
        # 1. 写入 SKU 数据库
        for _, row in edited.iterrows():
            if (
                row["写入 SKU 数据库"]
                and all([row["Item Description"], row["Commodity Code"], row["Weight"], row["Origin Country"]])
            ):
                append_sku_record(
                    row["Item Description"],
                    row["Commodity Code"],
                    row["Weight"],
                    row["Origin Country"]
                )
        # 2. 生成 DHL_ready_file.csv
        dhl_rows = []
        for i, row in edited.iterrows():
            formatted_code = format_commodity_code(row["Commodity Code"])
            dhl_rows.append([
                1,  # Unique Item Number 固定为1
                "INV_ITEM",  # Item
                row["Item Description"],
                formatted_code,
                1,  # Quantity
                "PCS",  # Units
                row["Selling Price"],
                "GBP",  # Currency
                row["Weight"],
                "",  # Weight 2
                row["Origin Country"],
                "", "", ""  # Reference Type, Details, Tax Paid
            ])
        dhl_df = pd.DataFrame(dhl_rows)
        dhl_df.columns = [
            "Unique Item Number", "Item", "Item Description", "Commodity Code", "Quantity",
            "Units", "Value", "Currency", "Weight", "Weight 2", "Country of Origin",
            "Reference Type", "Reference Details", "Tax Paid"
        ]
        st.subheader("📋 DHL 导出数据预览")
        st.dataframe(dhl_df, use_container_width=True)
        csv = dhl_df.to_csv(index=False, header=False)
        st.download_button(
            label="📥 下载 DHL_ready_file.csv",
            data=csv,
            file_name="DHL_ready_file.csv",
            mime="text/csv"
        )
        st.success("✅ 已写入 SKU 数据库并生成 DHL 文件！")

# Display memory database info
if st.sidebar.checkbox("📊 显示记忆数据库信息"):
    st.sidebar.subheader("智能记忆数据库")
    
    if os.path.exists("data/sku_memory_db.csv"):
        memory_df = pd.read_csv("data/sku_memory_db.csv")
        if not memory_df.empty:
            st.sidebar.write(f"📈 已记忆商品数量: {len(memory_df)}")
            st.sidebar.write("📋 记忆字段:")
            st.sidebar.write("• 海关编码 (Commodity Code)")
            st.sidebar.write("• 重量 (Weight)")
            st.sidebar.write("• 产地 (Country of Origin)")
            
            if st.sidebar.button("🗑️ 清空记忆数据库"):
                os.remove("data/sku_memory_db.csv")
                st.sidebar.success("记忆数据库已清空！")
                st.rerun()
        else:
            st.sidebar.write("📝 记忆数据库为空")
    else:
        st.sidebar.write("📝 记忆数据库尚未创建")
