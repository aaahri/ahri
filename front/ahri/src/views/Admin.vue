<template>
  <div id="admin" class="admin" :style="{backgroundImage: 'url(' + bg + ')'}">
    <div id="skin">
      <div class="area">
        <div class="hide">
          <div class="close" @click="close">×</div>
        </div>
        <div
          v-for="i in arr"
          :style="'background:url('+i.url+') no-repeat center;background-size: 100% 100%'"
          class="item"
          @click="changeSkin(i.url)"
        >
          <div></div>
        </div>
      </div>
    </div>
    <div id="nav" class="nav">
      <div class="logo">
        <div id="show" @click="showMenu">
          <span class="iconfont ahricategory"></span>
        </div>
        <router-link to="/admin/welcome">{{$t('lang.admin.nav.logo')}}</router-link>
      </div>
      <div class="btn">
        <span class="iconfont ahriicon_skin" @click="open"></span>
        <span class="iconfont ahrihome" @click="home"></span>
        <span class="iconfont ahritranslate" @click="changeLang"></span>
        <span class="time" @click="settime">{{time.hour}} : {{time.minute}} : {{time.second}}</span>
      </div>
    </div>
    <div id="decorate">
      {{$t('lang.admin.nav.logo')}}
      <div @click="hideMenu">
        <span class="iconfont ahriLeft-"></span>
      </div>
    </div>
    <div id="menu" class="menu">
      <div class="userinfo">
        <div class="card front">
          <img :src="user.avatar" alt="user">
          <div>
            <span>{{user.username}}</span>
            <p>{{user.description}}</p>
          </div>
        </div>
        <div class="card back">
          <button @click="myinfo">{{$t('lang.admin.menu.myinfo')}}</button>
          <button @click="logout">{{$t('lang.admin.menu.logout')}}</button>
        </div>
      </div>
      <div class="link">
        <div class="ul">
          <ul>
            <li class="line"></li>
            <router-link to="/admin/category">
              <li class="item">
                <span class="iconfont ahricategory"></span>
                {{$t('lang.admin.menu.category')}}
              </li>
            </router-link>
            <router-link to="/admin/article">
              <li class="item">
                <span class="iconfont ahribook"></span>
                {{$t('lang.admin.menu.allart')}}
              </li>
            </router-link>
            <router-link to="/admin/newart">
              <li class="item">
                <span class="iconfont ahriwrite"></span>
                {{$t('lang.admin.menu.addart')}}
              </li>
            </router-link>
            <router-link v-if="user.role >= 10" to="/admin/comment">
              <li class="item">
                <span class="iconfont ahriwrite"></span>
                {{$t('lang.admin.menu.comment')}}
              </li>
            </router-link>
            <li class="line"></li>
            <router-link to="/admin/mysql">
              <li class="item">
                <span class="iconfont ahrimysql"></span>
                MySql
              </li>
            </router-link>
            <li class="line"></li>
            <router-link to="/admin/myinfo">
              <li class="item">
                <span class="iconfont ahriinfo"></span>
                {{$t('lang.admin.menu.myinfo')}}
              </li>
            </router-link>
            <router-link v-if="user.role==100" to="/admin/user">
              <li class="item">
                <span class="iconfont ahriuser"></span>
                {{$t('lang.admin.menu.user')}}
              </li>
            </router-link>
            <router-link to="/admin/sysinfo">
              <li class="item">
                <span class="iconfont ahrisetting"></span>
                {{$t('lang.admin.menu.setting')}}
              </li>
            </router-link>
            <router-link v-if="user.role==100" to="/admin/bug">
              <li class="item">
                <span class="iconfont ahribug"></span>
                BUG
              </li>
            </router-link>
          </ul>
        </div>
      </div>
      <div class="copyright">
        <div class="con">
          <span>© 2019 aaahri.com</span>
          <br>
          <span>
            <a target="_blank" href="https://www.sojson.com/api/beian/aaahri.com">{{$t('lang.reg')}}</a>
          </span>
        </div>
      </div>
    </div>
    <div id="content" class="content">
      <router-view/>
    </div>
  </div>
</template>

<script>
import url from "@/assets/server";
import Qs from "qs";
import msg from "@/assets/tips";
export default {
  name: "admin",
  data() {
    return {
      user: { username: "", role: 0 },
      screenWidth: window.innerWidth,
      time: { hour: "00", minute: "00", second: "00" },
      bg: url + "/media/bg.jpg",
      arr: []
    };
  },
  beforeMount() {
    if (this.$store.state.user != null) {
      this.user = this.$store.state.user;
    } else {
      this.user = { role: 0 };
    }
    let self = this;
    this.axios
      .get(url + "/api/bg_setting/", {
        params: {
          bg: "bg",
          user_id: self.user._id.$oid
        }
      })
      .then(response => {
        if (response.data.code === 200) {
          if (JSON.parse(response.data.data) !== null)
            this.bg = JSON.parse(response.data.data).url;
        } else {
          console.log(response);
        }
      })
      .catch(response => {
        console.log(response);
      });
  },
  methods: {
    changeSkin(val) {
      this.bg = val;
      this.close();
      let self = this;
      this.axios
        .put(
          url + "/api/bg_setting/",
          Qs.stringify({
            url: val,
            user_id: self.user._id.$oid
          })
        )
        .then(response => {
          if (response.data.code !== 200) {
            msg("背景图片更新出错..", "#FF9966");
            console.log(response.data);
          }
        })
        .catch(response => {
          console.log(response);
        });
    },
    open() {
      let self = this;
      if (this.arr.length >= 0) {
        this.axios
          .get(url + "/api/bg_setting/", {
            params: {
              bg: "ma",
              user_id: self.user._id.$oid
            }
          })
          .then(response => {
            if (response.data.code === 200) {
              self.arr = JSON.parse(response.data.data);
            } else {
              console.log(response.data);
            }
          })
          .catch(response => {
            console.log(response);
          });
      }
      document.getElementById("skin").style.top = "0";
    },
    close() {
      document.getElementById("skin").style.top = "-100%";
    },
    settime() {
      if (window.timer) {
        window.clearTimeout(window.timer);
      }
      let myDate;
      let self = this;
      window.timer = setInterval(function() {
        myDate = new Date();
        let hour = myDate.getHours();
        let minute = myDate.getMinutes();
        let second = myDate.getSeconds();
        hour > 9 ? (self.time.hour = hour) : (self.time.hour = "0" + hour);
        minute > 9
          ? (self.time.minute = minute)
          : (self.time.minute = "0" + minute);
        second > 9
          ? (self.time.second = second)
          : (self.time.second = "0" + second);
      }, 1000);
    },
    changeLang() {
      this.$i18n.locale == "zh"
        ? (this.$i18n.locale = "en")
        : (this.$i18n.locale = "zh");
    },
    to(val) {
      this.$router.push({ name: val });
    },
    showMenu() {
      document.getElementById("menu").style.left = "0";
      document.getElementById("menu").style.background = "rgba(0, 0, 0, 0.9)";
      document.getElementById("decorate").style.left = "0";
      document.getElementsByClassName("front")[0].style.border =
        "solid 1px #aaa";
      document.getElementsByClassName("back")[0].style.border =
        "solid 1px #aaa";
    },
    hideMenu() {
      document.getElementById("menu").style.left = "-280px";
      document.getElementById("menu").style.background = "rgba(0, 0, 0, 0.2)";
      document.getElementById("decorate").style.left = "-280px";
      document.getElementsByClassName("front")[0].style.border = "none";
      document.getElementsByClassName("back")[0].style.border = "none";
    },
    changeLang() {
      this.$i18n.locale == "zh"
        ? (this.$i18n.locale = "en")
        : (this.$i18n.locale = "zh");
    },
    logout() {
      localStorage.removeItem("auth");
      this.$router.push("/");
      window.location.reload();
      // location.href("http://192.168.1.2:8080/");
    },
    myinfo() {
      this.$router.push("/admin/myinfo");
    },
    home() {
      this.$router.push("/");
    }
  },
  mounted() {
    window.onresize = () => {
      return (() => {
        this.screenWidth = window.innerWidth;
      })();
    };
    if (window.innerWidth < 1000) {
      document.getElementById("menu").style.left = "-280px";
      document.getElementById("menu").style.background = "rgba(0, 0, 0, 0.2)";
      document.getElementById("content").style.left = "0";
      document.getElementById("show").style.width = "40px";
      this.menu = false;
    } else {
      document.getElementById("menu").style.left = "0";
      document.getElementById("menu").style.background = "rgba(0, 0, 0, 0.2)";
      document.getElementById("content").style.left = "280px";
      document.getElementById("show").style.width = "0";
      this.menu = true;
    }
    this.settime();
    if (this.user.role < 10) {
      this.$router.push({ path: "/" });
    }
  },
  watch: {
    screenWidth(val) {
      if (val < 1000) {
        document.getElementById("menu").style.left = "-280px";
        document.getElementById("menu").style.background = "rgba(0, 0, 0, 0.2)";
        document.getElementById("content").style.left = "0";
        document.getElementById("show").style.width = "40px";
        this.menu = false;
      } else {
        document.getElementById("menu").style.left = "0";
        document.getElementById("menu").style.background = "rgba(0, 0, 0, 0.2)";
        document.getElementById("content").style.left = "280px";
        document.getElementById("show").style.width = "0";
        this.menu = true;
      }
      document.getElementById("decorate").style.left = "-280px";
      document.getElementsByClassName("front")[0].style.border = "none";
      document.getElementsByClassName("back")[0].style.border = "none";
    }
  }
};
</script>

<style lang="scss" scoped>
.admin {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  padding: 0;
  margin: 0;
  // background: url("../assets/1011715.jpg") no-repeat center;
  background-position: center center;
  background-repeat: no-repeat;
  background-size: 100% 100%;
  transition: 1s;
  z-index: 10;
  background-attachment: fixed;
  display: flex;
  justify-content: center;
  font-family: sans-serif;
}
.admin:before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  box-shadow: inset 0 0 2000px rgba(0, 0, 0, 0.3);
  background: inherit;
  filter: blur(6px);
  z-index: 0;
  margin: -20px;
}
#skin {
  z-index: 999999;
  position: fixed;
  top: -100%;
  left: 0;
  right: 0;
  height: 100%;
  display: flex;
  justify-content: center;
  transition: 0.8s;
  .area {
    position: absolute;
    top: 10px;
    width: 750px;
    left: 50%;
    transform: translateX(-50%);
    min-width: 400px;
    height: 350px;
    background: rgba(0, 0, 0, 0.8);
    border-radius: 8px;
    overflow: auto;
    .hide {
      height: 50px;
      width: 100%;
      background: rgba(0, 0, 0, 0.5);
      .close {
        height: 30px;
        width: 30px;
        float: right;
        margin: 10px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.2);
        line-height: 30px;
        text-align: center;
        color: #fff;
        cursor: pointer;
        transition: 0.2s;
        &:hover {
          background: rgba(100, 100, 100, 0.2);
          color: #aaa;
        }
      }
    }
    .item {
      width: 220px;
      height: 120px;
      margin: 10px 15px;
      float: left;
      background-size: cover;
      div {
        height: 100%;
        width: 100%;
        background: rgba(255, 255, 255, 0.3);
        transition: 0.4s;
        cursor: pointer;
        &:hover {
          background: none;
        }
        &:active {
          background: rgba(0, 0, 0, 0.3);
        }
      }
    }
  }
  @media screen and (min-width: 1100px) {
    .area {
      width: 1000px;
    }
  }
}
#nav {
  background: rgba(0, 0, 0, 0.3);
  padding: 0 20px;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 80px;
  line-height: 80px;
  box-shadow: 0 1px 1px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  -moz-user-select: none;
  -webkit-user-select: none;
  -ms-user-select: none;
  -khtml-user-select: none;
  user-select: none;
  .logo {
    font-size: 20px;
    color: #fff;
    letter-spacing: 2px;
    display: flex;
    // justify-content: space-between;
    align-items: center;
    width: 250px;
    cursor: pointer;
    transition: 0.2s;
    &:hover {
      color: #ccc;
      & > a {
        color: #aaa;
      }
    }
    #show {
      width: 40px;
      height: 40px;
      transition: 0.5s;
      overflow: hidden;
      line-height: 40px;
      margin-right: 10px;
      padding-top: 2px;
      cursor: pointer;
      &:hover {
        background: rgba(0, 0, 0, 0.6);
        border-radius: 4px;
        & > span {
          color: #aaa;
        }
      }
      span {
        padding-left: 5px;
        font-size: 30px;
      }
    }
    a {
      color: #ddd;
      font-size: 20px;
      text-decoration: none;
      transition: 0.2s;
    }
  }
  .btn {
    height: 100%;
    width: 280px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    span {
      height: 40px;
      width: 40px;
      font-size: 20px;
      line-height: 40px;
      text-align: center;
      color: #ddd;
      background: rgba(255, 255, 255, 0.3);
      border-radius: 4px;
      cursor: pointer;
      transition: 0.4s;
      &:hover {
        background: rgba(255, 255, 255, 0.4);
      }
      &:active {
        background: rgba(150, 150, 150, 0.2);
      }
    }
    .time {
      width: 120px;
    }
  }
}
#menu {
  background: rgba(0, 0, 0, 0.3);
  position: fixed;
  top: 80px;
  left: 0;
  bottom: 0;
  width: 280px;
  transition: 0.5s;
  z-index: 160;
  -moz-user-select: none;
  -webkit-user-select: none;
  -ms-user-select: none;
  -khtml-user-select: none;
  user-select: none;
}
#menu .userinfo {
  width: 94%;
  height: 80px;
  transition: 1s;
  margin: 10px;
  position: relative;
}
#menu .userinfo .card {
  position: absolute;
  width: 100%;
  height: 100%;
  overflow: hidden;
  backface-visibility: hidden;
  transition: transform 0.4s linear;
}
#menu .userinfo .front {
  transform: perspective(600px) rotateY(0deg);
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: left;
  align-items: center;
  cursor: pointer;
}
#menu .userinfo .back {
  transform: perspective(600px) rotateY(180deg);
  background: rgba(0, 0, 0, 0.6);
  text-align: center;
}
#menu .userinfo:hover > .front {
  transform: perspective(600px) rotateY(-180deg);
}
#menu .userinfo:hover > .back {
  transform: perspective(600px) rotateY(0deg);
}
#menu .userinfo .front img {
  height: 70%;
  border-radius: 50%;
  margin-left: 5%;
}
#menu .userinfo .front div {
  height: 70%;
  margin-left: 5%;
  color: #fff;
  text-align: left;
}
#menu .userinfo .front div span {
  font-size: 18px;
  font-weight: bold;
  letter-spacing: 2px;
}
#menu .userinfo .front div p {
  font-size: 12px;
  overflow: hidden;
  height: 16px;
  letter-spacing: 1px;
}
#menu .userinfo .back button {
  width: 60%;
  height: 36%;
  margin-top: 3%;
  background: none;
  border: solid 1px rgba(255, 255, 255, 1);
  color: #ddd;
  transition: 0.5s;
  cursor: pointer;
  outline: none;
}
#menu .userinfo .back button:hover {
  border-color: rgba(255, 255, 255, 0.5);
  color: #aaa;
  outline: none;
}
#menu .link {
  width: 100%;
  position: absolute;
  top: 110px;
  bottom: 80px;
  overflow: auto;
}
#menu .link .ul {
  width: 260px;
  display: flex;
  justify-content: center;
}
#menu .link .ul ul {
  padding: 0;
  margin: 0;
}
#menu .link .ul ul .item {
  text-align: left;
  list-style: none;
  background: rgba(255, 255, 255, 0.2);
  height: 40px;
  width: 220px;
  margin: 8px 0 8px 10px;
  line-height: 40px;
  padding-left: 20px;
  box-sizing: border-box;
  border-radius: 4px;
  transition: 0.5s;
  cursor: pointer;
}
#menu .link .ul ul .item:hover {
  background: rgba(255, 255, 255, 0.4);
  color: #ddd;
}
#menu .link .ul ul .item:hover > a {
  color: #eee;
}
#menu .link .ul ul .item:active {
  background: rgba(150, 150, 150, 0.2);
}
#menu .link .ul ul .item:active > a {
  color: #aaa;
}
#menu .link .ul ul a {
  color: #eee;
  text-decoration: none;
}
#menu .link .ul ul a span {
  font-size: 20px;
  color: #eee;
  margin: 0 5px;
}
#menu .link .ul ul .line {
  list-style: none;
  background: rgba(255, 255, 255, 0.2);
  height: 2px;
  width: 230px;
  margin: 0 0 0 5px;
}
#menu .copyright {
  width: 100%;
  position: absolute;
  left: 0;
  bottom: 0;
  height: 60px;
  text-align: center;
  background: rgba(0, 0, 0, 0.4);
  line-height: 25px;
  color: #aaa;
}
#menu .copyright a {
  color: #aaa;
}
#content {
  overflow: auto;
  position: fixed;
  top: 80px;
  left: 280px;
  right: 0;
  bottom: 0;
  transition: 0.5s;
  z-index: 150;
  padding: 15px;
}
#decorate {
  position: fixed;
  top: 0;
  left: -280px;
  width: 280px;
  height: 80px;
  background: rgba(0, 0, 0, 0.9);
  z-index: 160;
  transition: 0.5s;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 20px;
  color: #fff;
  letter-spacing: 2px;
}
#decorate div {
  width: 40px;
  height: 40px;
  transition: 0.6s;
  overflow: hidden;
  line-height: 40px;
  text-align: center;
  margin-left: 10px;
  transition: 0.6s;
  border-radius: 4px;
}
#decorate div:hover {
  background: rgba(255, 255, 255, 0.2);
}
#decorate div:hover > span {
  color: #fff;
}
#decorate div span {
  font-size: 30px;
  transition: 0.6s;
  color: #aaa;
  cursor: pointer;
}
</style>
