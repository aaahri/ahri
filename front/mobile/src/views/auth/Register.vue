<template>
  <div id="register" class="register">
    <div class="box">
      <h1>{{$t('lang.auth.register.title')}}</h1>
      <input
        class="username"
        type="text"
        name="username"
        :placeholder="$t('lang.auth.register.username')"
        autocomplete="off"
        v-model:value="username"
      >
      <input
        class="password"
        type="password"
        name="password"
        :placeholder="$t('lang.auth.register.password')"
        v-model:value="password"
      >
      <input
        class="mail"
        type="text"
        name="mail"
        v-model:value="email"
        :placeholder="$t('lang.auth.register.email')"
      >
      <div class="mailbox">
        <input
          class="mailcode"
          type="text"
          name="code"
          :placeholder="$t('lang.auth.register.code')"
          v-model:value="code"
        >
        <button @click="getcode" class="code">{{btndoce}}</button>
      </div>
      <button @click="register" class="btnLogin">{{$t('lang.auth.register.signup')}}</button>
      <router-link to="/auth/login">{{$t('lang.auth.register.goto')}}</router-link>
      <router-link to="/index">{{$t('lang.auth.register.index')}}</router-link>
    </div>
  </div>
</template>

<script>
import msg from "@/assets/tips";
import url from "@/assets/server";
export default {
  name: "register",
  data() {
    return {
      btndoce: this.$t("lang.auth.register.send"),
      username: "",
      password: "",
      email: "",
      code: ""
    };
  },
  created: function() {
    let self = this;
    document.onkeydown = function(e) {
      let key = window.event.keyCode;
      if (key === 13) {
        self.register(); //方法
      }
    };
  },
  methods: {
    getcode() {
      if (this.btndoce !== this.$t("lang.auth.register.send")) {
        document.getElementsByClassName("mailcode")[0].focus();
        return false;
      }
      var reg = new RegExp(
        "^[a-z0-9]+([._\\-]*[a-z0-9])*@([a-z0-9]+[-a-z0-9]*[a-z0-9]+.){1,63}[a-z0-9]+$"
      );
      if (this.email === "") {
        msg(this.$t("lang.auth.register.emailNull"), "#fff");
        document.getElementsByClassName("mail")[0].focus();
        return false;
      } else if (!reg.test(this.email)) {
        msg(this.$t("lang.auth.register.emailError"), "red");
        document.getElementsByClassName("mail")[0].focus();
        return false;
      } else {
        let self = this;
        this.axios
          // .get("http://django.0x0001.com/api/auth/", {
          .get(url + "/api/auth/register/", {
            params: {
              email: self.email
            }
          })
          .then(response => {
            if (response.data.code === 200) {
              msg(this.$t("lang.auth.register.hasSent"), "#2ecc71");
              window.code = response.data.data.code;
              window.email = response.data.data.email;
              self.btndoce = "60s";
              let t = 59;
              if (window.timer) {
                window.clearInterval(window.timer);
              }
              window.timer = window.setInterval(function() {
                if (t > 0) {
                  self.btndoce = t + "s";
                } else {
                  self.btndoce = self.$t("lang.auth.register.send");
                  window.clearInterval(window.timer);
                }
                t -= 1;
              }, 1000);
              document.getElementsByClassName("mailcode")[0].focus();
            } else if (response.data.code === 400) {
              msg(this.$t("lang.auth.register.emailError"), "red");
            } else if (response.data.code === 401) {
              msg(this.$t("lang.auth.register.emailHas"), "red");
            } else {
              console.log(response);
            }
          })
          .catch(response => {
            msg("未知错误..", "#FF9966");
            console.log(response);
          });
      }
    },
    register() {
      if (this.username == "") {
        msg(this.$t("lang.auth.register.usernameNull"), "#fff");
        document.getElementsByClassName("username")[0].focus();
        return false;
      }
      if (this.password == "") {
        msg(this.$t("lang.auth.register.passwordNull"), "#fff");
        document.getElementsByClassName("password")[0].focus();
        return false;
      }
      if (window.email === undefined) {
        msg(this.$t("lang.auth.register.nocode"), "#fff");
        document.getElementsByClassName("mailcode")[0].focus();
        return false;
      }
      if (this.email !== window.email) {
        msg(this.$t("lang.auth.register.emailChange"), "#fff");
        console.log(window.email);
        document.getElementsByClassName("mail")[0].focus();
        return false;
      }
      if (window.code !== this.code) {
        msg(this.$t("lang.auth.register.codeError"), "red");
        document.getElementsByClassName("mailcode")[0].focus();
        return false;
      }
      let self = this;
      this.axios({
        url: url + "/api/auth/register/",
        method: "post",
        //发送格式为json
        data: JSON.stringify({
          form: {
            username: self.username,
            password: self.password,
            email: self.email
          }
        }),
        headers: {
          "Content-Type": "application/json"
        }
      }).then(
        function(response) {
          if (response.data.code === 200) {
            self.$router.push("/auth/login");
          } else if (response.data.code === 401) {
            msg(self.$t("lang.auth.register.userHas"), "red");
          } else {
            console.log(response);
          }
        },
        function(response) {
          msg("未知错误..", "#FF9966");
          console.log(response);
        }
      );
    }
  }
};
</script>

<style lang="scss" scoped>
#register {
  width: 100%;
  // height: 150%;
  background: #34495e;
  display: flex;
  justify-content: center;
  // align-items: center;
  .msg {
    position: fixed;
    top: -60px;
    margin: 0 auto;
    width: 400px;
    height: 50px;
    background: #191919;
    border-radius: 6px;
    line-height: 50px;
    color: red;
    transition: 1s;
  }
}
#register .box {
  width: 300px;
  padding: 10px;
  background: #191919aa;
  text-align: center;
}
#register .box h1 {
  color: white;
  text-transform: uppercase;
  font-weight: 500;
}
#register .box .username,
#register .box .password,
#register .box .mail {
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
#register .box .username:focus,
#register .box .password:focus,
#register .box .mail:focus {
  width: 280px;
  border-color: #2ecc71;
}
#register .mailbox {
  display: flex;
  justify-content: space-between;
}
#register .box .mailcode {
  border: 0;
  background: none;
  display: block;
  margin: 0 auto;
  margin-right: 0;
  text-align: center;
  border: solid 2px #3498db;
  padding: 14px 10px;
  width: 100px;
  outline: none;
  color: white;
  border-radius: 24px 0 0 24px;
  transition: 0.4s;
}
#register .box .mailcode:focus {
  width: 220px;
  border-color: #2ecc71;
}
#register .box .code {
  border: 0;
  background: none;
  display: block;
  margin: 0 auto;
  margin-left: 0;
  text-align: center;
  border: solid 2px #2ecc71;
  padding: 14px 10px;
  width: 100px;
  outline: none;
  color: white;
  border-radius: 0 24px 24px 0;
  transition: 0.4s;
  cursor: pointer;
}
#register .box .code:hover {
  background: #2ecc71;
}
#register .box .code:active {
  background: #2b8d54;
}
#register .box .btnLogin {
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
#register .box .btnLogin:hover {
  background: #2ecc71;
}
#register .box .btnLogin:active {
  background: #2b8d54;
}
#register .box a {
  float: right;
  color: #ddd;
  transition: 0.25s;
  margin-left: 15px;
}
#register .box a:hover {
  color: #999;
}
#register .box a:active {
  color: #333;
}
</style>
