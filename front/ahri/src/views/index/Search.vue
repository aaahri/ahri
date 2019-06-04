<template>
  <div id="search" class="search">
    <div class="title">
      <div class="logo prohibit_copy">C</div>
      <div class="search_box">
        <input
          v-on:keyup.13="search"
          v-model:value="content"
          class="search_txt"
          type="text"
          :placeholder="$t('lang.search.search')"
        >
        <a class="search_btn" @click="search" href="javascript:void(0)">
          <span class="iconfont ahrii-search"></span>
        </a>
      </div>
      <div class="right prohibit_copy">
        <router-link v-if="user.role == 0" to="/auth/login">{{$t('lang.search.login')}}</router-link>
        <router-link v-if="user.role == 0" to="/auth/register">{{$t('lang.search.register')}}</router-link>
        <router-link v-if="user.role > 0" to="/admin">{{$t('lang.search.logout')}}</router-link>
        <router-link v-if="user.role >= 10" to="/admin">{{$t('lang.search.admin')}}</router-link>
        <button @click="changLang">{{$t('lang.search.lang')}}</button>
      </div>
    </div>
    <div @click="index" class="back">←</div>
    <div id="result" class="result">
      <div v-if="article.length == 0 && category.length == 0" class="msg">{{$t('lang.search.msg')}}</div>
      <div v-if="category.length > 0" class="category">
        <div v-for="i in category" class="item">
          <div class="name">{{i.name}}</div>
          <div class="info">
            <div class="img">
              <img :src="i.thumbnail" alt>
            </div>
            <div class="detailed">
              <div class="desc">{{i.desc}}</div>
              <div class="opera">
                By {{i.author_name}} @ {{i.change_date}}
                <a
                  href="javascript:void(0)"
                  @click="to(i.first)"
                >{{$t('lang.search.more')}}>></a>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-if="article.length > 0 && category.length > 0" class="hr"></div>
      <div v-if="article.length > 0" class="article">
        <div v-for="i in article" class="item">
          <span class="art_title">{{i.title}}</span>
          <br>
          <span class="desc">{{i.desc}}</span>
          <br>
          <span class="opera">
            By {{i.author_name}} @ {{i.change_date}}
            <a
              @click="to(i._id)"
              href="javascript:void(0)"
            >{{$t('lang.search.read')}}</a>
          </span>
        </div>
      </div>
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
import loading from "@/assets/loading";
import url from "@/assets/server";
import msg from "@/assets/tips";
export default {
  name: "search",
  data() {
    return {
      content: "",
      category: [],
      article: [],
      user: {
        role: 0
      }
    };
  },
  methods: {
    to(id) {
      this.$router.push({ path: "/read", query: { id: id.$oid } });
    },
    index() {
      this.$router.push({ path: "/index" });
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
    search(val) {
      this.$router.push({ path: "/search", query: { content: this.content } });
      let load = loading(document.getElementById("result"));
      let self = this;
      this.axios
        .get(url + "/api/index/search/", {
          params: {
            content: self.content
          }
        })
        .then(response => {
          if (response.data.code === 200) {
            self.category = JSON.parse(response.data.data.category);
            self.article = JSON.parse(response.data.data.article);
            document.getElementById("result").removeChild(load);
          } else if (response.data.code === 400) {
            msg(this.$t("lang.category.authFail"), "red");
          } else {
            msg("未知错误..", "#FF9966");
            console.log(response.data);
          }
        })
        .catch(response => {
          msg("未知错误..", "#FF9966");
          console.log(response);
        });
    }
  },
  mounted() {
    this.content = this.$route.query.content;
    this.search(this.content);
    if (localStorage.getItem("auth") != null) {
      this.user = JSON.parse(
        JSON.parse(localStorage.getItem("auth")).user.data
      );
    } else {
      this.user = { role: 0 };
    }
  }
};
</script>

<style lang="scss" scoped>
#search {
  position: relative;
  top: 0;
  left: 0;
  height: 100%;
  overflow-y: auto;
  .title {
    z-index: 9000;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 80px;
    background: #fff;
    box-shadow: 0 6px 10px rgba(0, 0, 0, 0.3);
    display: flex;
    justify-content: space-between;
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
    .search_box {
      height: 40px;
      width: 400px;
      margin: 20px 0;
      box-sizing: border-box;
      border-radius: 40px;
      border: solid 2px #666;
      padding: 0 0 0 15px;
      .search_txt {
        margin-top: 1px;
        height: 30px;
        width: 340px;
        border: none;
        outline: none;
      }
      .search_btn {
        float: right;
        height: 32px;
        width: 32px;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        border: solid 2px #666;
        transition: 0.3s;
        text-decoration: none;
        &:hover {
          background: #ddd;
        }
        span {
          color: #000;
          font-weight: 600;
        }
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
      button {
        background: none;
        border: none;
        border: solid 1px rgba(0, 0, 0, 0.3);
        outline: none;
        box-shadow: 2px 2px 2px rgba(0, 0, 0, 0.3);
      }
    }
  }
  .back {
    margin-top: 100px;
    font-size: 38px;
    font-weight: 600;
    padding-left: 15px;
    width: 70px;
    transition: 0.2s;
    cursor: pointer;
    color: #555;
    &:hover {
      color: #000;
    }
  }
  .result {
    position: relative;
    z-index: 500;
    padding: 20px 50px 10px 50px;
    .msg {
      width: 600px;
      height: 200px;
      line-height: 200px;
      margin: 0 auto;
      background: #ddd;
      font-size: 36px;
      text-align: center;
    }
    .category {
      .item {
        padding: 10px;
        margin-bottom: 10px;
        box-sizing: border-box;
        background: #ddd;
        cursor: pointer;
        &:hover > .info > .detailed > .desc {
          color: #222;
        }
        &:hover > .info > .detailed > .opera {
          color: #222;
        }
        &:hover > .name {
          letter-spacing: 5px;
        }
        .name {
          font-size: 20px;
          font-weight: 600;
          color: #1985bb;
          transition: 0.4s;
        }
        .info {
          height: 120px;
          padding-top: 10px;
          box-sizing: border-box;
          position: relative;
          .img {
            float: left;
            margin-right: 20px;
            img {
              width: 100px;
              height: 100px;
            }
          }
          .detailed {
            .desc {
              transition: 0.2s;
              height: 66px;
              overflow: hidden;
              margin-bottom: 12px;
              font-weight: 600;
              word-wrap: break-word;
            }
            .opera {
              text-align: left;
              transition: 0.2s;
              font-weight: 600;
              a {
                color: #2eb6fa;
                transition: 0.2s;
                &:hover {
                  color: #666;
                }
              }
            }
          }
        }
      }
    }
    .hr {
      border: solid 1px #333;
      margin: 30px 0;
    }
    .article {
      .item {
        border-bottom: solid 1px #333;
        margin-top: 15px;
        padding-bottom: 5px;
        span {
          transition: 0.4s;
        }
        .art_title {
          font-size: 20px;
        }
        &:hover > .art_title {
          color: #000;
          letter-spacing: 5px;
        }
        .opera {
          a {
            color: #2599d3;
            &:hover {
              color: #666;
            }
          }
        }
      }
    }
  }
}
</style>
