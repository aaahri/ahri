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
      <button @click="changeLang" class="lang">{{$t('lang.auth.register.lang')}}</button>
      <router-link to="/auth/forget">{{$t('lang.auth.login.forget')}}</router-link>
      <router-link to="/auth/register">{{$t('lang.auth.login.goto')}}</router-link>
      <router-link to="/index">{{$t('lang.auth.login.index')}}</router-link>
    </div>
    <!-- <button @click="github">GitHub</button> -->
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
    changeLang() {
      if (this.$i18n.locale == "zh") {
        this.$i18n.locale = "en";
        // document.getElementsByClassName("right")[0].style.width = "200px";
      } else {
        this.$i18n.locale = "zh";
        // document.getElementsByClassName("right")[0].style.width = "140px";
      }
    },
    github() {
      window.location.href = "http://dev.aaahri.com?client=adf0f7eee38aa96b";
    },
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
            self.$store.commit('SAVE_USER', auth);
            self.$router.push("/index");
          } else if (response.data.code === 400) {
            msg(self.$t("lang.auth.login.loginfail"), "red");
          } else if (response.data.code === 401) {
            msg(self.$t("lang.auth.login.disable"), "red");
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
  padding: 40px;
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
#login .box .lang {
  background: none;
  cursor: pointer;
  border: none;
  color: #fff;
  font-size: 16px;
  float: left;
  outline: none;
  transition: 0.4s;
}
#login .box .lang:hover {
  color: #999;
}
</style>
