<template>
  <div id="login" class="login">
    <div class="box prohibit_copy">
      <h1>{{$t('lang.auth.login.title')}}</h1>
      <input
        v-on:keyup.13="login"
        type="text"
        v-model:value="username"
        :placeholder="$t('lang.auth.login.username')"
        autocomplete="off"
      >
      <input
        v-on:keyup.13="login"
        type="password"
        v-model:value="password"
        :placeholder="$t('lang.auth.login.password')"
      >
      <button class="btnLogin" @click="login">{{$t('lang.auth.login.signin')}}</button>
      <router-link to="/auth/register">{{$t('lang.auth.login.goto')}}</router-link>
      <router-link to="/index">{{$t('lang.auth.login.index')}}</router-link>
    </div>
  </div>
</template>

<script>
import msg from "@/assets/tips";
import url from "@/assets/server";
import Qs from "qs";
export default {
  name: "login",
  data() {
    return {
      username: "",
      password: ""
    };
  },
  methods: {
    login() {
      let self = this;
      this.axios({
        url: url + "/api/auth/login/",
        method: "post",
        data: JSON.stringify({
          form: { username: self.username, password: self.password }
        }),
        headers: {
          "Content-Type": "application/json"
        }
      }).then(
        function(response) {
          if (response.data.code === 200) {
            let auth = {
              user: response.data
            };
            localStorage.setItem("auth", JSON.stringify(auth));
            var referrer = sessionStorage.getItem("referrer");
            if (referrer != null) {
              self.$router.push(referrer);
            } else {
              self.$router.push("/index");
            }
          } else if (response.data.code === 400) {
            msg(self.$t("lang.auth.login.loginfail"), "red");
          } else {
            msg("未知错误..", "#FF9966");
            console.log(response.data);
          }
        },
        function(response) {
          msg("未知错误..", "#FF9966");
          console.log(response);
        }
      );
    }
  },
  mounted() {}
};
</script>

<style>
#login {
  width: 100%;
  height: 100%;
  background: #34495e;
  display: flex;
  justify-content: center;
  align-items: center;
  /* background: url("../../assets/340911.jpg") no-repeat center; */
  /* background-size: cover; */
}
#login .box {
  width: 300px;
  padding: 10px;
  background: #191919aa;
  text-align: center;
}
#login .box h1 {
  color: white;
  text-transform: uppercase;
  font-weight: 500;
}
#login .box input[type="text"],
#login .box input[type="password"] {
  border: 0;
  background: none;
  display: block;
  margin: 20px auto;
  text-align: center;
  border: solid 2px #3498db;
  padding: 14px 10px;
  width: 200px;
  outline: none;
  color: white;
  border-radius: 24px;
  transition: 0.4s;
}
#login .box input[type="text"]:focus,
#login .box input[type="password"]:focus {
  width: 280px;
  border-color: #2ecc71;
}
#login .box .btnLogin {
  border: 0;
  background: none;
  display: block;
  margin: 20px auto;
  text-align: center;
  border: solid 2px #2ecc71;
  padding: 14px 10px;
  width: 220px;
  outline: none;
  color: white;
  border-radius: 24px;
  transition: 0.4s;
  cursor: pointer;
}
#login .box .btnLogin:hover {
  background: #2ecc71;
}
#login .box .btnLogin:active {
  background: #2b8d54;
}
#login .box a {
  float: right;
  color: #ddd;
  transition: 0.25s;
  margin-left: 15px;
}
#login .box a:hover {
  color: #999;
}
#login .box a:active {
  color: #333;
}
</style>
