const form = document.querySelector("#login-form");

let accessToken = null;

const checkPassword = () => {
  const formData = new FormData(form);
  const password1 = formData.get("password");
  const password2 = formData.get("password2");
  if (password1 === password2) {
    return true;
  } else {
    return false;
  }
};

const handleSubmit = async (event) => {
  event.preventDefault();
  const formData = new FormData(form);
  const sha256Password = sha256(formData.get("password"));
  //input 태그의 name키워드가 해당 값을 불러올 수 있다.
  formData.set("password", sha256Password);

  const div = document.querySelector("#info");

  const res = await fetch("/login", {
    method: "POST",
    body: formData,
  });
  const data = await res.json();
  accessToken = data.access_token;
  window.localStorage.setItem("token", accessToken);
  alert("로그인 되었습니다.");

  window.location.pathname = "/";
};

form.addEventListener("submit", handleSubmit);
