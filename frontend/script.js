function login() {
    let user = document.getElementById("username").value;
    let pass = document.getElementById("password").value;

    // Predefined credentials
    if (user === "admin" && pass === "VMOUSE@2026") {
        window.location.href = "dashboard.html";
    } else {
        document.getElementById("error").innerText =
            "Invalid Username or Password";
    }
}
