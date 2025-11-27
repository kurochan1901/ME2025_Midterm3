// 開啟與關閉Modal
function open_input_table() {
    document.getElementById("addModal").style.display = "block";

    // today's date
    document.getElementById("order_date").value = new Date().toISOString().split("T")[0];
}
function close_input_table() {
    document.getElementById("addModal").style.display = "none";
}

function delete_data(value) {
    // 發送 DELETE 請求到後端
    fetch(`/product?order_id=${value}`, {
        method: "DELETE",
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("伺服器回傳錯誤");
        }
        return response.json(); // 假設後端回傳 JSON 格式資料
    })
    .then(result => {
        console.log(result); // 在這裡處理成功的回應
        close_input_table(); // 關閉 modal
        location.assign('/'); // 重新載入頁面
    })
    .catch(error => {
        console.error("發生錯誤：", error);
    });
}

document.addEventListener("DOMContentLoaded", function() {
    // 取得表單元素
    const category = document.getElementById("category");
    const product = document.getElementById("product");
    const price = document.getElementById("price");
    const qty = document.getElementById("qty");
    const subtotal = document.getElementById("subtotal");

    if (!category) return; // 如果找不到 category 元素，則退出

    category.addEventListener("change", function() {
        // 根據選擇的類別取得商品列表
        const type = category.value;

        fetch(`/product/category?type=${encodeURIComponent(type)}`)
            .then(response => response.json())
            .then(data => {
                
                product.innerHTML = `<option disabled selected>請選擇商品</option>`;
                data.forEach(p => {
                    product.innerHTML += `<option value="${p.name}">${p.name}</option>`;
                });
            });
    });
    
});