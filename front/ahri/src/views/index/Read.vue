<template>
  <div class="read" id="read">
    <div class="catalog prohibit_copy" id="catalog">
      <button id="home" @click="home">{{$t('lang.read.home')}}</button>
      <button id="hide" @click="hideMenu">{{$t('lang.read.hide')}}</button>
      <div class="item" v-for="(i,n) in list" @click="show(n)">{{i.title}}</div>
    </div>
    <div class="read_area" id="read_area">
      <button id="show" @click="showMenu">{{$t('lang.read.show')}}</button>
      <div class="title">{{art.title}}</div>
      <div class="hr"></div>
      <div class="info">By {{art.author_name}} @ {{art.change_date}}</div>
      <div class="content" v-html="art.content"></div>
      <div class="opera">
        <button @click="prev">{{$t('lang.read.last')}}</button>
        <button @click="next">{{$t('lang.read.next')}}</button>
      </div>
      <div class="hr"></div>
      <div class="msg">留 言：</div>
      <div class="comment">
        <div v-for="i in comment" class="comment_item">
          <div class="img">
            <img src="http://127.0.0.1:9000/static/ahri.jpg" alt>
          </div>
          <div class="content">
            <p>{{i.content}}</p>
          </div>
          <div class="msg_info">--By {{i.user_name}} @ {{i.date}}</div>
        </div>
        <div class="message">
          <textarea maxlength="120" name id v-model:value="lmsg"></textarea>
          <br>
          <span>剩余 {{len}} 字</span>
          <br>
          <button @click="leavemessage">{{$t('lang.read.leavemsg')}}</button>
        </div>
      </div>
      <div class="copyright prohibit_copy">
        <div class="con">
          <span>© 2019 aaahri.com</span>
          <span>
            <a target="_blank" href="https://www.sojson.com/api/beian/aaahri.com">{{$t('lang.reg')}}</a>
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import url from "@/assets/server";
import Qs from "qs";
import msg from "@/assets/tips";
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
  name: "read",
  data() {
    return {
      user: {
        role: 0
      },
      lmsg: "",
      screenWidth: 0,
      list: [],
      num: 0,
      art: {
        title: "",
        date: "",
        author: "",
        content: ""
      },
      comment: [],
      len: 120
    };
  },
  methods: {
    leavemessage() {
      let auth = JSON.parse(localStorage.getItem("auth")) || false;
      if (auth) {
        let self = this;
        this.axios({
          url: url + "/api/comment/",
          method: "post",
          data: JSON.stringify({
            content: self.lmsg,
            article: self.art._id.$oid,
            user: self.user
          }),
          headers: {
            "Content-Type": "application/json"
          }
        }).then(
          function(response) {
            if (response.data.code === 200) {
              self.comment.push(JSON.parse(response.data.data));
              self.lmsg = "";
              msg(self.$t("lang.newart.addsuccess"), "#2ecc71");
            } else if (response.data.code === 400) {
              msg(self.$t("lang.newart.authFail"), "red");
            } else if (response.data.code === 401) {
              msg(self.$t("lang.newart.titleHas"), "red");
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
      } else {
        alert("请登录！");
      }
    },
    home() {
      this.$router.push({ path: "/index" });
    },
    showMenu() {
      document.getElementById("catalog").style.left = "0";
    },
    hideMenu() {
      document.getElementById("catalog").style.left = "-280px";
    },
    show(val) {
      this.num = val;
      this.change();
    },
    prev() {
      if (this.num > 0) {
        this.num--;
        this.change();
      }
    },
    next() {
      if (this.num < this.list.length - 1) {
        this.num++;
        this.change();
      }
    },
    change() {
      let load = loading(document.getElementById("read"));
      this.art = this.list[this.num];
      this.$router.push({ path: "/read", query: { id: this.art._id.$oid } });
      document.body.scrollTop = document.documentElement.scrollTop = 0;
      let self = this;
      this.axios
        .get(url + "/api/comment/", {
          params: {
            article: self.art._id.$oid
          }
        })
        .then(response => {
          if (response.data.code === 200) {
            self.comment = JSON.parse(response.data.data);
            document.getElementById("read").removeChild(load);
            if (self.isInPage(window.load)) {
              document.getElementById("read").removeChild(window.load);
            }
          } else {
            alert("failed");
          }
        })
        .catch(response => {
          console.log(response);
        });
    },
    isInPage(node) {
      return node === document.body ? false : document.body.contains(node);
    }
  },
  mounted() {
    window.load = loading(document.getElementById("read"));
    window.onresize = () => {
      return (() => {
        this.screenWidth = window.innerWidth;
      })();
    };
    if (window.innerWidth < 1200) {
      document.getElementById("catalog").style.left = "-280px";
      document.getElementById("read_area").style.left = "0";
      document.getElementById("show").style.display = "block";
      document.getElementById("hide").style.display = "block";
    } else {
      document.getElementById("catalog").style.left = "0";
      document.getElementById("read_area").style.left = "280px";
      document.getElementById("show").style.display = "none";
      document.getElementById("hide").style.display = "none";
    }
    let id = this.$route.query.id;
    let self = this;
    this.axios
      .get(url + "/api/read/", {
        params: {
          id: id
        }
      })
      .then(response => {
        if (response.data.code === 200) {
          self.list = JSON.parse(response.data.data);
          for (let i = 0; i < this.list.length; i++) {
            if (this.list[i]._id.$oid == id) {
              self.show(i);
            }
          }
        } else {
          alert("failed");
        }
      })
      .catch(response => {
        console.log(response);
      });
    if (localStorage.getItem("auth") != null) {
      this.user = JSON.parse(
        JSON.parse(localStorage.getItem("auth")).user.data
      );
    } else {
      this.user = { role: 0 };
    }
    highlightCode();
  },
  updated() {
    highlightCode();
  },
  watch: {
    screenWidth(val) {
      if (val < 1200) {
        document.getElementById("catalog").style.left = "-280px";
        document.getElementById("read_area").style.left = "0";
        document.getElementById("show").style.display = "block";
        document.getElementById("hide").style.display = "block";
      } else {
        document.getElementById("catalog").style.left = "0";
        document.getElementById("read_area").style.left = "280px";
        document.getElementById("show").style.display = "none";
        document.getElementById("hide").style.display = "none";
      }
    },
    lmsg(val) {
      this.len = 120 - val.length;
    }
  }
};
</script>

<style lang="scss" scoped>
.read {
  width: 100%;
  height: 100%;
  position: relative;
  .catalog {
    position: fixed;
    width: 280px;
    top: 0;
    left: 0;
    bottom: 0;
    padding-top: 50px;
    background: #343b42;
    transition: 0.4s;
    z-index: 9999;
    padding-bottom: 70px;
    display: inline-block;
    overflow-y: auto;
    #home {
      position: absolute;
      top: 5px;
      left: 5px;
      height: 30px;
      width: 80px;
      border: none;
      cursor: pointer;
      outline: none;
      color: #fff;
      background: rgba(0, 0, 0, 0.2);
      transition: 0.4s;
      &:hover {
        background: rgba(0, 0, 0, 0.4);
        color: #ccc;
      }
      &:active {
        background: rgba(0, 0, 0, 0.6);
        color: #999;
      }
    }
    #hide {
      position: absolute;
      top: 5px;
      right: 5px;
      height: 30px;
      width: 80px;
      border: none;
      cursor: pointer;
      outline: none;
      color: #fff;
      background: rgba(0, 0, 0, 0.2);
      transition: 0.4s;
      &:hover {
        background: rgba(0, 0, 0, 0.4);
        color: #ccc;
      }
      &:active {
        background: rgba(0, 0, 0, 0.6);
        color: #999;
      }
    }
    .item {
      text-align: center;
      cursor: pointer;
      width: 90%;
      margin: 5px 5%;
      height: 40px;
      line-height: 40px;
      color: #fff;
      background: rgba(0, 0, 0, 0.2);
      transition: 0.4s;
      overflow: hidden;
      &:hover {
        background: rgba(0, 0, 0, 0.4);
        color: #ccc;
      }
      &:active {
        background: rgba(0, 0, 0, 0.6);
        color: #999;
      }
    }
  }
  .read_area {
    position: absolute;
    top: 0;
    left: 280px;
    right: 0;
    bottom: 0;
    background: #eee;
    width: 800px;
    margin: 0 auto;
    transition: 0.4s;
    #show {
      position: absolute;
      top: 5px;
      left: 5px;
      height: 30px;
      width: 80px;
      border: none;
      cursor: pointer;
      outline: none;
      color: #333;
      background: rgba(180, 180, 180, 0.3);
      transition: 0.4s;
      &:hover {
        background: rgba(180, 180, 180, 0.2);
        color: #999;
      }
      &:active {
        background: rgba(180, 180, 180, 0.4);
        color: #333;
      }
    }
    .title {
      text-align: center;
      margin-top: 150px;
      font-size: 35px;
      font-weight: 600;
    }
    .hr {
      height: 0;
      width: 100%;
      margin: 10px 0;
      border: solid 1px rgba(0, 0, 0, 0.6);
    }
    .info {
      text-align: right;
      margin: 15px;
      font-size: 20px;
    }
    .content {
    }
    .msg {
      font-size: 20px;
      font-weight: 600;
    }
    .comment {
      margin: 20px 0 100px 0;
      width: 100%;
      .comment_item {
        width: 90%;
        margin: 10px 5%;
        padding: 5px 30px;
        box-sizing: border-box;
        border-bottom: solid 1px rgba(0, 0, 0, 0.4);
        .img {
          float: left;
          margin-right: 20px;
          img {
            height: 50px;
            width: 50px;
            border-radius: 50%;
          }
        }
        .content {
          p {
            word-wrap: break-word;
            word-break: break-all;
            overflow: hidden;
          }
        }
        .msg_info {
          text-align: right;
        }
      }
      .message {
        width: 90%;
        margin: 0 5%;
        textarea {
          width: 100%;
          height: 120px;
          outline: none;
          font-size: 20px;
          font-weight: 600;
          padding: 10px;
          box-sizing: border-box;
          resize: none;
        }
        button {
          float: right;
          border: none;
          height: 40px;
          width: 180px;
          font-size: 20px;
          font-weight: 600;
          cursor: pointer;
          transition: 0.2s;
          background: #ccc;
          outline: none;
          &:hover {
            background: #ddd;
            color: #333;
          }
          &:active {
            background: rgba(0, 0, 0, 0.5);
            color: #333;
          }
        }
      }
    }
    .opera {
      margin: 20px 0 20px 0;
      display: flex;
      justify-content: center;
      button {
        margin: 0 50px;
        border: none;
        height: 40px;
        width: 180px;
        font-size: 20px;
        font-weight: 600;
        cursor: pointer;
        transition: 0.2s;
        background: #ccc;
        outline: none;
        &:hover {
          background: #ddd;
          color: #333;
        }
        &:active {
          background: rgba(0, 0, 0, 0.5);
          color: #333;
        }
      }
    }
    .copyright {
      text-align: center;
      margin: 0 0 20px 0;
      span {
        margin: 15px;
        a {
          color: #333;
          transition: 0.2s;
          text-decoration: none;
          &:hover {
            color: #000;
            text-decoration: underline;
          }
        }
      }
    }
  }
}
</style>