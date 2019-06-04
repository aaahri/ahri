<template>
  <div id="index" class="index">
    <div class="nav">
      <div class="logo prohibit_copy">C</div>
      <div class="right prohibit_copy">
        <router-link v-if="user.role == 0" to="/auth/login">{{$t('lang.index.login')}}</router-link>
        <router-link v-if="user.role == 0" to="/auth/register">{{$t('lang.index.register')}}</router-link>
        <button
          @click="logout"
          class="logout"
          v-if="user.role > 0"
          to="/admin"
        >{{$t('lang.index.logout')}}</button>
        <router-link v-if="user.role >= 10" to="/admin">{{$t('lang.index.admin')}}</router-link>
        <button class="lang" @click="changLang">{{$t('lang.index.lang')}}</button>
      </div>
    </div>
    <div class="exhibition">
      <div class="search">
        <Search></Search>
      </div>
      <div class="goto prohibit_copy">
        <!-- <router-link to="/serial">{{$t('lang.index.serial')}}</router-link>
        <router-link to="/serial">{{$t('lang.index.show')}}</router-link>-->
        <router-link to="/index">
          <div class="icon iconfont ahrihome"></div>
          <div class="function">{{$t('lang.index.home')}}</div>
        </router-link>
        <router-link to="/index/indexlast">
          <div class="icon iconfont ahriarticle"></div>
          <div class="function">{{$t('lang.index.article')}}</div>
        </router-link>
        <router-link to="/" style="cursor: not-allowed;">
          <div class="icon iconfont ahriproject24"></div>
          <div class="function">{{$t('lang.index.isay')}}</div>
        </router-link>
        <router-link to="/index/indexcate">
          <div class="icon iconfont ahricategory"></div>
          <div class="function">{{$t('lang.index.category')}}</div>
        </router-link>
        <router-link to="/" style="cursor: not-allowed;">
          <div class="icon iconfont ahriImages"></div>
          <div class="function">{{$t('lang.index.image')}}</div>
        </router-link>
        <router-link to="/" style="cursor: not-allowed;">
          <div class="icon iconfont ahriinfo"></div>
          <div class="function">{{$t('lang.index.info')}}</div>
        </router-link>
      </div>
      <div class="hr"></div>
      <div id="content">
        <div class="view">
          <router-view/>
        </div>
        <div class="content" v-html="article.content"></div>
      </div>
      <br>
      <br>
      <br>
      <br>
      <br>
      <br>
      <br>
      <br>
      <br>
      <br>
      <br>
      <br>
      <br>
      <br>
      <br>
      <br>
      <br>
      <br>
      <br>
      <br>
    </div>
  </div>
</template>

<script>
import url from "@/assets/server";
import loading from "@/assets/loading";
import Search from "@/components/Search.vue";
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
  components: {
    Search
  },
  data() {
    return {
      article: { content: "" },
      user: {
        role: 0
      }
    };
  },
  beforeMount() {},
  methods: {
    logout() {
      localStorage.removeItem("auth");
      this.$router.push("/");
      window.location.reload();
    },
    changLang() {
      if (this.$i18n.locale == "zh") {
        this.$i18n.locale = "en";
      } else {
        this.$i18n.locale = "zh";
      }
    }
  },
  mounted() {
    let load = loading(document.getElementById("content"));
    highlightCode();
    document.getElementById("index").onscroll = function() {
      var t =
        document.getElementById("index").scrollTop || document.body.scrollTop;
      if (t >= 200) {
      } else {
      }
    };
    let self = this;
    this.axios
      .get(url + "/api/index/")
      .then(response => {
        if (response.data.code === 200) {
          self.article = JSON.parse(response.data.data);
          document.getElementById("content").removeChild(load);
        } else if (response.data.code === 300) {
          document.getElementById("content").removeChild(load);
        } else {
          alert("failed");
        }
      })
      .catch(response => {
        console.log(response);
      });
    if (this.$store.state.user != null) {
      this.user = this.$store.state.user;
    } else {
      this.user = { role: 0 };
    }
  },
  updated() {
    highlightCode();
  }
};
</script>

<style lang="scss">
#index {
  position: relative;
  top: 0;
  left: 0;
  height: 100%;
  overflow-y: auto;
  .nav {
    z-index: 9999;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 80px;
    background: #fff;
    box-shadow: 0 6px 10px rgba(0, 0, 0, 0.3);
    .logo {
      height: 100%;
      width: 70px;
      line-height: 80px;
      text-align: center;
      margin: 0 30px;
      font-size: 50px;
      font-family: "STKaiti";
      font-weight: bold;
      float: left;
      cursor: pointer;
      transition: 0.2s;
      &:hover {
        color: #000;
      }
    }
    .right {
      display: flex;
      justify-content: space-between;
      align-items: center;
      height: 100%;
      width: 160px;
      float: right;
      margin: 0 20px;
      a {
        font-family: "Avenir", Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        color: #2c3e50;
        font-weight: 600;
        text-decoration: none;
        transition: 0.2s;
        &:hover {
          color: #000;
        }
      }
      .logout {
        border: none;
        background: none;
        font-family: "Avenir", Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        color: #2c3e50;
        font-size: 16px;
        font-weight: 600;
        text-decoration: none;
        transition: 0.2s;
        outline: none;
        cursor: pointer;
        &:hover {
          color: #000;
        }
      }
      .lang {
        background: none;
        border: none;
        border: solid 1px rgba(0, 0, 0, 0.3);
        outline: none;
        box-shadow: 2px 2px 2px rgba(0, 0, 0, 0.3);
      }
    }
  }
  .exhibition {
    min-width: 700px;
    z-index: 9000;
    margin-top: 100px;
    .search {
      width: 100%;
      display: flex;
      justify-content: center;
      padding: 50px 0;
    }
    .goto {
      height: 70px;
      width: 80%;
      margin: 0 10%;
      line-height: 40px;
      text-align: center;
      a {
        display: inline-block;
        width: 90px;
        height: 50px;
        margin: 0 5px;
        position: relative;
        color: #54616d;
        font-weight: 600;
        transition: 0.6s;
        &:hover {
          color: #000;
          font-weight: 700;
        }
        .icon {
          position: absolute;
          top: 0;
          left: 50%;
          transform: translateX(-50%);
          width: 40px;
          font-size: 35px;
        }
        .function {
          position: absolute;
          top: 30px;
          left: 50%;
          transform: translateX(-50%);
          width: 100%;
        }
      }
    }
    .hr {
      width: 90%;
      margin: 0 5%;
      background: #374553;
      border: solid 1px #333;
    }
    #content {
      position: relative;
      min-height: 400px;
      min-width: 700px;
      padding: 50px 100px;
      .view {
        padding: 0 10% 30px 10%;
      }
      .content {
        width: 70%;
        margin: 0 auto;
        img {
          max-width: 70px;
          margin: 0 5%;
        }
      }
    }
  }
}
.ql-syntax {
  font-size: 22px;
}
</style>

