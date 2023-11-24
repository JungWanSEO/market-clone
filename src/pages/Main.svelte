<script>
  import { onMount } from "svelte";
  import Footer from "../components/Footer.svelte";
  import { getDatabase, ref, onValue } from "firebase/database";

  let hour = new Date().getHours();
  let min = new Date().getMinutes().toString().padStart(2, "0");

  $: items = [];
  const db = getDatabase();
  const itemsRef = ref(db, "items/");

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

  // svelte의 원리
  // javascript파일의 경우 화면이 처음 렌더링이 될때,
  // 한번만 실행 하고 그 다음은 데이터를 보여주지 않음
  onMount(() => {
    //값이 바뀔 때마다 snapshot이 바뀌게 된다.(실시간)
    onValue(itemsRef, (snapshot) => {
      const data = snapshot.val();
      items = Object.values(data).reverse();
    });
  });
</script>

<header>
  <div class="info-bar">
    <div class="info-bar__time">{hour}:{min}</div>
    <div class="info-bar__icons">
      <img src="assets/chart-bar.svg" alt="chart-bar" />
      <img src="assets/wifi.svg" alt="wifi" />
      <img src="assets/battery.svg" alt="battery" />
    </div>
  </div>
  <div class="menu-bar">
    <div class="menu-bar__location">
      <div>역삼1동</div>
      <div class="menu-bar__location-icon">
        <img src="assets/arrow-down.svg" alt="" />
      </div>
    </div>
    <div class="menu-bar__icons">
      <img src="assets/search.svg" alt="" />
      <img src="assets/menu.svg" alt="" />
      <img src="assets/alert.svg" alt="" />
    </div>
  </div>
</header>

<main>
  {#each items as item}
    <div class="items-list">
      <div class="items-list__img">
        <img src={item.imgUrl} alt={item.title} />
      </div>
      <div class="items-list__info">
        <div class="items-list__info-title">{item.title}</div>
        <div class="items-list__info-meta">
          {item.place}
          {calcTime(item.insertAt)}
        </div>
        <div class="items-list__info-price">{item.price}</div>
        <div>{item.description}</div>
      </div>
    </div>
  {/each}
  <a class="write-btn" href="#/write">+ 글쓰기</a>
</main>

<Footer location="home" />
<div class="media-info-msg">화면사이즈를 줄여주세요.</div>

<style>
  .info-bar__time {
    color: blue;
  }
</style>
