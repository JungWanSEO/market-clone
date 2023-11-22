const calcTime = (timestamp) => {
  //한국시간 UTC+9가 되기 때문에 세계시간으로 맞춘다
  const curTime = new Date().getTime() - 9 * 60 * 60 * 1000;
  const time = new Date(curTime - timestamp);
  const year = time.getFullYear();
  console.log(year);
  const month = time.getMonth();
  const day = time.getDate();
  const hour = time.getHours();
  const minute = time.getMinutes();
  const second = time.getSeconds();

  if (month > 0) return `${month + 1}달 전`;
  else if (day > 0) return `${day}일 전`;
  else if (hour > 0) return `${hour}시간 전`;
  else if (minute > 0) return `${minute}분 전`;
  else if (second > 0) return `${second}초 전`;
  else return "방금 전";
};

const renderData = (data) => {
  const main = document.querySelector("main");

  data.reverse().forEach(async (obj) => {
    const div = document.createElement("div");
    div.className = "items-list";

    const imageDiv = document.createElement("div");
    imageDiv.className = "items-list__img";

    const image = document.createElement("img");
    const imgRes = await fetch(`/images/${obj.id}`);
    const blob = await imgRes.blob();
    const url = URL.createObjectURL(blob);
    image.src = url;

    const InfoDiv = document.createElement("div");
    InfoDiv.className = "items-list__info";

    const InfoTitleDiv = document.createElement("div");
    InfoTitleDiv.className = "items-list__info-title";
    InfoTitleDiv.innerText = obj.title;

    const InfoMetaDiv = document.createElement("div");
    InfoMetaDiv.className = "items-list__info-meta";
    InfoMetaDiv.innerText = obj.place + " " + calcTime(obj.insertAt);

    const InfoPriceDiv = document.createElement("div");
    InfoPriceDiv.className = "items-list__info-price";
    InfoPriceDiv.innerText = obj.price;

    InfoDiv.appendChild(InfoTitleDiv);
    InfoDiv.appendChild(InfoMetaDiv);
    InfoDiv.appendChild(InfoPriceDiv);

    imageDiv.appendChild(image);
    div.appendChild(imageDiv);
    div.appendChild(InfoDiv);

    main.appendChild(div);
  });
};

const fetchList = async () => {
  const accessToken = window.localStorage.getItem("token");
  const response = await fetch("/items", {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  });
  if (response.status == 401) {
    window.location.pathname = "/login.html";
    return;
  }
  const data = await response.json();
  renderData(data);
};

fetchList();
