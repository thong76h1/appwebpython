from flask import Flask, render_template, request, redirect, url_for, session, flash
import pyodbc
import math

app = Flask(__name__)
app.secret_key = "your_secret_key"
DATABASE_CONFIG = {
    'driver': '{ODBC Driver 17 for SQL Server}',  # Thay bằng driver bạn đã cài đặt
    'server': 'F51-DCS-204\sql2017',                       # Hoặc IP của SQL Server
    'database': 'TV41',                        # Tên cơ sở dữ liệu
    'username': 'sa',                            # Tên người dùng SQL Server
    'password': '@abc123@'                  # Mật khẩu
}

def truncate_text(text, max_length):
    if len(text) > max_length:
        return text[:max_length - 3] + "..."
    return text
# Hàm kết nối SQL Server
def get_db_connection():
    connection = pyodbc.connect(
        f"DRIVER={DATABASE_CONFIG['driver']};"
        f"SERVER={DATABASE_CONFIG['server']};"
        f"DATABASE={DATABASE_CONFIG['database']};"
        f"UID={DATABASE_CONFIG['username']};"
        f"PWD={DATABASE_CONFIG['password']}"
    )
    return connection
def getToppro():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Lấy dữ liệu cho trang hiện tại
    cursor.execute(
        "SELECT top 20 * FROM inputbds ORDER BY Price desc"
    )
    product = cursor.fetchall()
    conn.close()
    return product
def getQ():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Lấy dữ liệu cho trang hiện tại
    cursor.execute(
        "SELECT   * FROM district ORDER BY id desc"
    )
    product = cursor.fetchall()
    conn.close()
    return product
def getH():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Lấy dữ liệu cho trang hiện tại
    cursor.execute(
        "SELECT * FROM district ORDER BY id desc"
    )
    product = cursor.fetchall()
    conn.close()
    return product
def coutproT():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Lấy dữ liệu cho trang hiện tại
   
    cursor.execute("SELECT COUNT(*) FROM inputbds")
    total_records = cursor.fetchone()[0]
    return total_records
def coutproVp():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Lấy dữ liệu cho trang hiện tại
    cursor.execute("SELECT COUNT(*) FROM inputbdsvp")
    total_records = cursor.fetchone()[0]
    return total_records
# Đăng nhập
@app.route("/login", methods=["GET", "POST"])
def login():
    if "user" in session:  # Nếu đã đăng nhập, chuyển hướng về index
        return redirect(url_for("index"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Truy vấn thông tin người dùng
        cursor.execute("SELECT Password FROM Users WHERE Username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        
        if  user[0] == password:
            session["user"] = username 
            return redirect(url_for("index"))
        else:
            render_template("login.html")
    
    return render_template("login.html")

# Hiển thị dữ liệu (trang index)
@app.route("/")
def index():
    category = request.args.get("category")
    coutVP = coutproVp()
    coutT = coutproT()
    geta = getH()
    getb = getQ()
    if "user" not in session:  # Nếu chưa đăng nhập, chuyển về login
        return redirect(url_for("login"))
    
    if category == 'thue':
    # Lấy dữ liệu cho trang hiện tại
        topPro = getToppro()
        page = request.args.get("page", 1, type=int)  # Lấy số trang từ URL, mặc định là 1
        per_page = 12  # Số dòng hiển thị mỗi trang
    
        conn = get_db_connection()
        cursor = conn.cursor()
        user = session["user"] 
        # Lấy tổng số bản ghi
        cursor.execute("SELECT COUNT(*) FROM inputbds")
        total_records = cursor.fetchone()[0]
        
        # Tính toán giới hạn và offset
        total_pages = math.ceil(total_records / per_page)
        offset = (page - 1) * per_page
        cursor.execute(
            "SELECT * FROM inputbds ORDER BY id OFFSET ? ROWS FETCH NEXT ? ROWS ONLY",
            (offset, per_page)
        
        )
        product = cursor.fetchall()
    elif category == 'vp':
        topPro = getToppro()
        page = request.args.get("page", 1, type=int)  # Lấy số trang từ URL, mặc định là 1
        per_page = 12  # Số dòng hiển thị mỗi trang
        conn = get_db_connection()
        cursor = conn.cursor()
        user = session["user"] 
        # Lấy tổng số bản ghi
        cursor.execute("SELECT COUNT(*) FROM inputbdsVP")
        total_records = cursor.fetchone()[0]

        # Tính toán giới hạn và offset
        total_pages = math.ceil(total_records / per_page)
        offset = (page - 1) * per_page
        cursor.execute(
            "SELECT * FROM inputbdsVP ORDER BY id OFFSET ? ROWS FETCH NEXT ? ROWS ONLY",
            (offset, per_page)
        
        )
        product = cursor.fetchall()
    else:
        topPro = getToppro()
        page = request.args.get("page", 1, type=int)  # Lấy số trang từ URL, mặc định là 1
        per_page = 12  # Số dòng hiển thị mỗi trang
        
        conn = get_db_connection()
        cursor = conn.cursor()
        user = session["user"] 
        # Lấy tổng số bản ghi
        cursor.execute("SELECT COUNT(*) FROM inputbds")
        total_records = cursor.fetchone()[0]

        # Tính toán giới hạn và offset
        total_pages = math.ceil(total_records / per_page)
        offset = (page - 1) * per_page
        cursor.execute(
            "SELECT * FROM inputbds ORDER BY id OFFSET ? ROWS FETCH NEXT ? ROWS ONLY",
            (offset, per_page)
        
        )
        product = cursor.fetchall()
    
    conn.close()

    return render_template("index.html",geta=geta,getb = getb, product=product, current_page=page, total_pages=total_pages,username= user,topPro = topPro,coutVP = coutVP,coutt = coutT)


@app.route('/detail')
def detail():
    detail = request.args.get("detail")
    if "user" not in session:  # Nếu chưa đăng nhập, chuyển về login
        return redirect(url_for("login"))
    conn = get_db_connection()
    cursor = conn.cursor()
    user = session["user"] 
        # Lấy tổng số bản ghi
        # Tính toán giới hạn và offset
    # cursor.execute(
    #     "SELECT * FROM inputbds where id = ? ",(detail)
    # )
    query = "SELECT * FROM inputbds WHERE id LIKE ?"
    cursor.execute(query, ('%' + detail + '%',))
    product = cursor.fetchall()    
    flash(f"Đăng nhập thành công!", detail)
    return render_template("detail.html",product = product,detail=detail)
    
# Đăng xuất
@app.route("/logout")
def logout():
    session.pop("user", None)  # Xóa trạng thái đăng nhập
    flash("Đã đăng xuất.", "info")
    return redirect(url_for("login"))

    
app.jinja_env.filters['truncate_text'] = truncate_text
if __name__ == "__main__":
    app.run(debug=True)
