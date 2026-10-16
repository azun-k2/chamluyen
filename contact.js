// Quick-message form on the support page: posts to the Chăm luyện server (the back office shows it).
(function () {
  var form = document.getElementById("quick-form");
  if (!form) return;
  var API = "https://chamluyen-api.chamluyen-server.workers.dev/v1/contact";
  var vi = document.documentElement.lang === "vi";
  var T = vi
    ? { sending: "Đang gửi…", ok: "Đã gửi. Chúng tôi sẽ liên hệ với bạn qua số điện thoại này.", phone: "Số điện thoại chưa đúng (di động Việt Nam, 10 số).", many: "Bạn vừa gửi tin nhắn. Vui lòng đợi 10 phút rồi gửi lại, hoặc dùng email hay Zalo.", bad: "Vui lòng điền đủ thông tin.", net: "Chưa gửi được. Kiểm tra mạng rồi thử lại, hoặc dùng email hay Zalo." }
    : { sending: "Sending…", ok: "Sent. We will reach out on this phone number.", phone: "That phone number does not look right (a Vietnamese mobile number, 10 digits).", many: "You just sent a message. Please wait 10 minutes before sending another, or use email or Zalo.", bad: "Please fill in every field.", net: "Could not send. Check the connection and try again, or use email or Zalo." };
  var status = form.querySelector(".status"), button = form.querySelector("button");
  var kind = form.querySelectorAll("input[name=kind]"), groups = { buy: form.querySelector("[data-for=buy]"), support: form.querySelector("[data-for=support]") };
  function sync() {
    var k = form.querySelector("input[name=kind]:checked").value;
    Object.keys(groups).forEach(function (g) {
      groups[g].hidden = g !== k;
      groups[g].querySelectorAll("input").forEach(function (i) { i.disabled = g !== k; });
    });
  }
  kind.forEach(function (r) { r.addEventListener("change", sync); });
  sync();
  function say(text, error) { status.textContent = text; status.className = "status" + (error ? " error" : ""); }
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var k = form.querySelector("input[name=kind]:checked").value;
    var opt = groups[k].querySelector("input:checked");
    var name = form.elements.name.value.trim(), phone = form.elements.phone.value.trim();
    if (!name || !phone || !opt) return say(T.bad, true);
    button.disabled = true; say(T.sending);
    fetch(API, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ name: name, phone: phone, kind: k, option: opt.value, note: form.elements.note.value.trim(), website: form.elements.website.value }) })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (b) { return { status: r.status, body: b }; }); })
      .then(function (r) {
        if (r.status === 201) { say(T.ok); form.reset(); sync(); return; }
        say(r.body.error === "bad_phone" ? T.phone : r.status === 429 ? T.many : T.bad, true);
      })
      .catch(function () { say(T.net, true); })
      .then(function () { button.disabled = false; });
  });
})();
