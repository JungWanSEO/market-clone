<script>
  import Login from "./pages/Login.svelte";
  import Main from "./pages/Main.svelte";
  import Loading from "./pages/Loading.svelte";
  import NotFound from "./pages/NotFound.svelte";
  import Signup from "./pages/Signup.svelte";
  import Write from "./pages/Write.svelte";
  import Router from "svelte-spa-router";
  import "./css/style.css";
  import {
    GoogleAuthProvider,
    getAuth,
    signInWithCredential,
  } from "firebase/auth";
  import { user$ } from "./store";
  import { onMount } from "svelte";
  import MyPage from "./pages/MyPage.svelte";

  let isLoading = true;

  const auth = getAuth();

  const checkLogin = async () => {
    console.log("랜더링!!");
    const token = localStorage.getItem("token");
    if (!token) return (isLoading = false);
    const credential = GoogleAuthProvider.credential(null, token);
    // Sign in with credential from the Google user.
    const result = await signInWithCredential(auth, credential);

    const user = result.user;
    user$.set(user);
    isLoading = false;
  };

  const routes = {
    "/": Main,
    "/signup": Signup,
    "/write": Write,
    "/mypage": MyPage,
    "*": NotFound,
  };

  onMount(() => checkLogin());
</script>

{#if isLoading}
  <Loading></Loading>
{:else if !$user$}
  <Login></Login>
{:else}
  <Router {routes}></Router>
{/if}
