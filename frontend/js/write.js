const handleSubmitForm = async (event) => {
  event.preventDefault();
  const body = new FormData(form);
  //세계시간 기준으로
  body.append("insertAt", new Date().getTime());
  try {
    const response = await fetch("/items", {
      method: "POST",
      body,
    });
    const data = await response.json();
    if (data === "200") {
      //성공하면 화면 페이지를 이동해라
      window.location.pathname = "/";
    }
  } catch (e) {
    console.error(e);
  }

  console.log("제출완료");
};

const form = document.getElementById("write-form");
form.addEventListener("submit", handleSubmitForm);
