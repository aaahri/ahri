<template>
  <div id="forget" class="forget">
    <div class="box">
      <h1>{{$t('lang.auth.forget.title')}}</h1>
      <input
        class="mail"
        type="text"
        name="mail"
        v-model:value="email"
        :placeholder="$t('lang.auth.forget.email')"
      >
      <div class="mailbox">
        <input
          class="mailcode"
          type="text"
          name="code"
          :placeholder="$t('lang.auth.forget.code')"
          v-model:value="code"
        >
        <button @click="getcode" class="code">{{btndoce}}</button>
      </div>
      <input
        class="password"
        type="password"
        name="password"
        :placeholder="$t('lang.auth.forget.password')"
        v-model:value="password"
      >
      <button @click="submit" class="btnLogin">{{$t('lang.auth.forget.submit')}}</button>
      <button @click="changeLang" class="lang">{{$t('lang.auth.register.lang')}}</button>
      <router-link to="/auth/login">{{$t('lang.auth.register.goto')}}</router-link>
      <router-link to="/index">{{$t('lang.auth.register.index')}}</router-link>
    </div>
  </div>
</template>

<script>
import msg from "@/assets/tips";
import url from "@/assets/server";
import Qs from "qs";
export default {
  name: "register",
  data() {
    return {
      btndoce: this.$t("lang.auth.forget.send"),
      email: "",
      password: "",
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
    changeLang() {
      if (this.$i18n.locale == "zh") {
        this.$i18n.locale = "en";
      } else {
        this.$i18n.locale = "zh";
      }
      this.btndoce = this.$t("lang.auth.forget.send");
    },
    getcode() {
      if (this.btndoce !== this.$t("lang.auth.forget.send")) {
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
        msg(this.$t("lang.auth.register.hasSent"), "#2ecc71");
        self.btndoce = "60s";
        let t = 59;
        let doce = this.$t("lang.auth.register.send");
        if (window.timer) {
          window.clearInterval(window.timer);
        }
        window.timer = window.setInterval(function() {
          if (t > 0) {
            self.btndoce = t + "s";
          } else {
            self.btndoce = doce;
            window.clearInterval(window.timer);
          }
          t -= 1;
        }, 1000);
        document.getElementsByClassName("mailcode")[0].focus();
        this.axios
          .get(url + "/api/auth/register/", {
            params: {
              email: self.email,
              op: 2
            }
          })
          .then(response => {
            if (response.data.code === 200) {
              window.code = response.data.data.code;
              window.email = response.data.data.email;
            } else if (response.data.code === 400) {
              msg(this.$t("lang.auth.register.emailError"), "red");
            } else if (response.data.code === 401) {
              msg(this.$t("lang.auth.forget.emailNull"), "red");
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
    submit() {
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
      if (this.password == "") {
        msg(this.$t("lang.auth.register.passwordNull"), "#fff");
        document.getElementsByClassName("password")[0].focus();
        return false;
      }
      let self = this;
      this.axios
        .put(
          url + "/api/auth/register/",
          Qs.stringify({
            email: self.email,
            password: self.password
          })
        )
        .then(response => {
          if (response.data.code === 200) {
            msg(self.$t("lang.auth.forget.changeSuccess"), "#2ecc71");
            self.$router.push("/auth/login");
          } else if (response.data.code === 401) {
            msg(this.$t("lang.auth.forget.emailNull"), "red");
          } else {
            msg("未知错误..(from forget put)", "#FF9966");
            console.log(response.data);
          }
        })
        .catch(response => {
          msg("未知错误..", "#FF9966");
          console.log(response);
        });
    }
  }
};
</script>

<style lang="scss" scoped>
#forget {
  width: 100%;
  height: 100%;
  background: #34495e;
  display: flex;
  justify-content: center;
  align-items: center;
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
#forget .box {
  width: 300px;
  padding: 40px;
  background: #191919;
  text-align: center;
}
#forget .box h1 {
  color: white;
  text-transform: uppercase;
  font-weight: 500;
}
#forget .box .username,
#forget .box .password,
#forget .box .mail {
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
#forget .box .username:focus,
#forget .box .password:focus,
#forget .box .mail:focus {
  width: 280px;
  border-color: #2ecc71;
}
#forget .mailbox {
  display: flex;
  justify-content: space-between;
}
#forget .box .mailcode {
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
#forget .box .mailcode:focus {
  width: 220px;
  border-color: #2ecc71;
}
#forget .box .code {
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
#forget .box .code:hover {
  background: #2ecc71;
}
#forget .box .code:active {
  background: #2b8d54;
}
#forget .box .btnLogin {
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
#forget .box .btnLogin:hover {
  background: #2ecc71;
}
#forget .box .btnLogin:active {
  background: #2b8d54;
}
#forget .box a {
  float: right;
  color: #ddd;
  transition: 0.25s;
  margin-left: 15px;
}
#forget .box a:hover {
  color: #999;
}
#forget .box a:active {
  color: #333;
}
#forget .box .lang {
  background: none;
  cursor: pointer;
  border: none;
  color: #fff;
  font-size: 16px;
  float: left;
  outline: none;
  transition: 0.4s;
}
#forget .box .lang:hover {
  color: #999;
}
</style>
