<template>
  <div id="index" class="index">
    <div id="mask"></div>
    <div id="menu" class="menu">
      <div class="hide" @click="hide">←</div>
      <button @click="goto('/index/indexcate')" class="item item1">{{$t('lang.index.category')}}</button>
      <button @click="goto('/index/indexlast')" class="item">{{$t('lang.index.article')}}</button>
    </div>
    <div class="nav">
      <span class="iconfont ahricategory" @click="show"></span>
      <div class="auth">
        <span class="iconfont ahritranslate" @click="changLang"></span>
        <span v-if="user.role > 0">
          <a href="javascript:void(0)" @click="logout">{{$t('lang.index.logout')}}</a>
        </span>
        <span v-if="user.role <= 0">
          <router-link to="/auth/login">{{$t('lang.index.login')}}</router-link>
        </span>
        <span v-if="user.role <= 0">
          <router-link to="/about">{{$t('lang.index.register')}}</router-link>
        </span>
      </div>
    </div>
    <div class="container">
      <div class="search_box">
        <input
          v-on:keyup.13="search"
          v-model="what"
          type="text"
          class="search"
          :placeholder="$t('lang.index.search')"
        >
        <div @click="search" class="search_btn">
          <span class="iconfont ahrii-search"></span>
        </div>
      </div>
      <div class="view">
        <router-view/>
      </div>
      <div id="content" class="content" v-html="article.content"></div>
    </div>
  </div>
</template>

<script>
import url from "@/assets/server";
import loading from "@/assets/loading";
import "highlight.js/styles/vs2015.css";
import hljs from "highlight.js";
const highlightCode = () => {
  const preEl = document.querySelectorAll("pre");

  preEl.forEach(el => {
    hljs.highlightBlock(el);
  });
};
export default {
  name: "index",
  data() {
    return {
      article: { content: "" },
      what: "",
      user: 0
    };
  },
  methods: {
    goto(val) {
      this.$router.push(val);
      this.hide();
    },
    logout() {
      localStorage.removeItem("auth");
      this.user.role = 0;
      this.$router.push("/");
    },
    changLang() {
      if (this.$i18n.locale == "zh") {
        this.$i18n.locale = "en";
        // document.getElementsByClassName("right")[0].style.width = "200px";
      } else {
        this.$i18n.locale = "zh";
        // document.getElementsByClassName("right")[0].style.width = "140px";
      }
    },
    search() {
      this.$router.push({ path: "/search", query: { content: this.what } });
    },
    show() {
      document.getElementById("menu").style.left = "0";
      document.getElementById("mask").style.display = "block";
      document.body.style.overflow = "hidden";
    },
    hide() {
      document.getElementById("menu").style.left = "-100%";
      document.getElementById("mask").style.display = "none";
      document.body.style.overflow = "auto";
    }
  },
  mounted() {
    let load = loading(document.getElementById("content"));
    let self = this;
    this.axios
      .get(url + "/api/index/")
      .then(response => {
        if (response.data.code === 200) {
          self.article = JSON.parse(response.data.data);
          document.getElementById("content").removeChild(load);
        } else if (response.data.code === 300) {
          self.article = {
            content: ""
          };
          document.getElementById("content").removeChild(load);
        } else {
          alert("failed");
        }
      })
      .catch(response => {
        console.log(response);
      });
    highlightCode();
    if (localStorage.getItem("auth") != null) {
      this.user = JSON.parse(
        JSON.parse(localStorage.getItem("auth")).user.data
      );
    } else {
      this.user = { role: 0 };
    }
  },
  updated() {
    highlightCode();
  }
};
</script>

<style lang="scss" scoped>
.ql-syntax {
  font-size: 22px;
  overflow-x: auto;
  margin: 0 !important;
}
#index {
  .menu {
    position: fixed;
    top: 0;
    left: -70%;
    width: 70%;
    height: 100%;
    max-width: 240px;
    z-index: 9999;
    transition: 0.3s;
    background: #4d4d4d;
    .hide {
      float: right;
      margin: 10px;
      font-size: 18px;
      color: #fff;
      font-weight: 600;
    }
    .item {
      margin: 10px auto;
      height: 36px;
      width: 180px;
      background: rgba(0, 0, 0, 0.5);
      border-radius: 6px;
      transition: 0.3s;
      line-height: 36px;
      padding: 0 15px;
      box-sizing: border-box;
      color: #fff;
      text-decoration: none;
      display: block;
      border: none;
      &:active {
        background: rgba(0, 0, 0, 0.8);
      }
    }
    .item1 {
      margin-top: 45px;
    }
  }
  #mask {
    z-index: 9990;
    background: rgba(0, 0, 0, 0.5);
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: none;
  }
  .nav {
    z-index: 9900;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 60px;
    background: #4b4b4b;
    line-height: 60px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    span {
      color: #fff;
      font-size: 25px;
      margin: 10px;
      a {
        font-size: 16px;
        color: #fff;
      }
    }
    .auth {
      padding: 0 15px;
    }
  }
  .container {
    z-index: 9000;
    margin: 80px 0;
    .search_box {
      z-index: 999;
      position: relative;
      .search {
        position: absolute;
        width: 84%;
        top: 0;
        left: 8%;
        height: 36px;
        border-radius: 36px;
        border: solid 2px #333;
        outline: none;
        padding: 3px 20px;
        box-sizing: border-box;
        font-size: 18px;
      }
      .search_btn {
        position: absolute;
        top: 0;
        right: 8%;
        width: 36px;
        height: 36px;
        border-radius: 50%;
        text-align: center;
        line-height: 36px;
        background: rgba($color: #000000, $alpha: 0.1);
        span {
          color: #333;
          font-weight: 600;
        }
      }
    }
    .view {
      z-index: 99;
      padding-top: 60px;
    }
    .content {
      width: 80%;
      margin: 0 auto;
      p {
        margin: 0 !important;
      }
    }
  }
}
</style>
