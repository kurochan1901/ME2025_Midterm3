// 開啟與關閉Modal
function open_input_table() {
    document.getElementById("addModal").style.display = "block";
    document.getElementById("date").value = new Date().toISOString().split("T")[0];
}

function close_input_table() {
    document.getElementById("addModal").style.display = "none";
}

function delete_data(order_id) {
    fetch(`/product?order_id=${order_id}`, { method: "DELETE" })
        .then(r => r.json())
        .then(result => {
            alert(result.message);
            location.reload();
        });
}


document.addEventListener("DOMContentLoaded", function () {
    // 取得欄位元素
    const category = document.getElementById("category");
    const product  = document.getElementById("product");
    const price    = document.getElementById("price");
    const amount   = document.getElementById("amount");
    const total    = document.getElementById("total");

    category.addEventListener("change", function () {
        const cat = category.value;
        // 更新商品名稱
        fetch(`/product?category=${encodeURIComponent(cat)}`)
            .then(r => r.json())
            .then(data => {

                product.innerHTML = `<option disabled selected>請選擇商品</option>`;

                data.product.forEach(name => {
                    product.innerHTML += `<option value="${name}">${name}</option>`;
                });
            });
    });

    // 當選擇商品時，取得價格並更新價格欄位
    product.addEventListener("change", function () {
        const name = product.value;

        fetch(`/product?product=${encodeURIComponent(name)}`)
            .then(r => r.json())
            .then(data => {
                price.value = data.price;
                updateTotal();
            });
    });

    // 當數量改變時，更新小計欄位
    amount.addEventListener("input", updateTotal);

    function updateTotal() {
        const p = Number(price.value);
        const q = Number(amount.value);

        total.value = p > 0 && q > 0 ? p * q : 0;
    }
});

// 連接後端 POST /product
document.getElementById("submit-btn").addEventListener("click", function() {
    // 要傳送的資料
    const body = {
        date: document.getElementById("date").value,
        customer_name: document.getElementById("customer_name").value,
        product: product.value,
        amount: Number(amount.value),
        total: Number(total.value),
        status: document.getElementById("status").value,
        note: document.getElementById("note").value        
    };


        fetch("/product", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(body)
        })
        .then(response => {
            if (response.redirected) {
                window.location.href = response.url;
                return;
            }
        });
});
