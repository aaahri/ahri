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
                <br>
                <a
                  v-if="i.first != ''"
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
  .title {
    z-index: 9999;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 60px;
    box-shadow: 0 6px 10px rgba(0, 0, 0, 0.3);
    .logo {
      position: absolute;
      top: 10px;
      left: 20px;
      font-size: 34px;
      font-weight: 600;
    }
    .search_box {
      position: absolute;
      top: 15px;
      left: 80px;
      right: 80px;
      input {
        height: 30px;
        width: 100%;
        border-radius: 30px;
        border: solid 2px #333;
        background: none;
        box-sizing: border-box;
        outline: none;
        padding: 2px 20px;
      }
      a {
        position: absolute;
        right: 0;
        height: 30px;
        width: 30px;
        line-height: 30px;
        text-align: center;
        border-radius: 50%;
        text-decoration: none;
        font-weight: 600;
        color: #000;
        background: rgba(0, 0, 0, 0.1);
        outline: none;
      }
    }
    .right {
      position: absolute;
      right: 10px;
      top: 20px;
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
    z-index: 9000;
    margin-top: 80px;
  }
  .result {
    z-index: 500;
    padding: 10px;
    box-sizing: border-box;
    .category {
      .item {
        padding: 10px;
        margin-bottom: 10px;
        box-sizing: border-box;
        background: #eee;
        .name {
          font-size: 24px;
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
              height: 56px;
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
        background: #eee;
        margin-bottom: 10px;
        padding: 10px;
        box-sizing: border-box;
        .art_title {
          font-size: 28px;
          color: #2eb6fa;
        }
        .desc {
        }
        .opera {
        }
      }
    }
  }
}
</style>
