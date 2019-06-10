<template>
  <div id="articlepage" class="articlepage">
    <div class="head prohibit_copy">
      <h3>{{$t('lang.article.tab')}}</h3>
      <h5>{{$t('lang.article.private')}}</h5>
    </div>
    <select class="selectCate" v-model:value="selectCate" name id>
      <option value="全部">{{$t('lang.article.all')}}</option>
      <option v-for="i in category" :value="i.name">{{i.name}}</option>
    </select>
    <input
      v-model:value="filter"
      class="fillter"
      type="text"
      :placeholder="$t('lang.article.fillter')"
    >
    <select class="select" v-model:value="select" name id>
      <option value="5">5</option>
      <option value="10">10</option>
      <option value="15">15</option>
      <option value="20">20</option>
    </select>
    <div id="table" class="table">
      <div class="header prohibit_copy">
        <span class="col1">{{$t('lang.article.title')}}</span>
        <span class="col2">{{$t('lang.article.desc')}}</span>
        <span class="col3">{{$t('lang.article.date')}}</span>
        <span class="col4">{{$t('lang.article.opera')}}</span>
      </div>
      <div v-for="i in article_show[thisPage]" class="body" :title="'分类：'+i.category_name">
        <span v-if="i.p" class="col1 red">{{i.title}}</span>
        <span v-else class="col1">{{i.title}}</span>
        <span class="col2">{{i.desc}}</span>
        <span class="col3">{{i.change_date}}</span>
        <span class="col4">
          <button class="edit" @click="editArt(i._id, i.editor)">{{$t('lang.article.edit')}}</button>
          <button class="delete" @click="delArt(i._id)">{{$t('lang.article.delete')}}</button>
        </span>
        <form id="go1" action="http://127.0.0.1:9000/editor/ckeditor/" method="post">
          <input hidden type="text" name="user" v-model:value="user._id.$oid">
          <input hidden id="art_id1" type="text" name="type" value="n">
        </form>
        <form id="go2" action="http://127.0.0.1:9000/editor/ckeditor/" method="post">
          <input hidden type="text" name="user" v-model:value="user._id.$oid">
          <input hidden id="art_id2" type="text" name="type" value="n">
        </form>
      </div>
      <div class="msg" v-if="article.length == 0">{{$t('lang.article.msg')}}</div>
      <div class="paging" v-if="num > 1">
        <span class="prev iconfont ahriLeft-" @click="prev"></span>
        <span v-for="i in num" @click="changePage(i)">{{i}}</span>
        <span class="next iconfont ahriRight-" @click="next"></span>
      </div>
    </div>
  </div>
</template>

<script>
import loading from "@/assets/loading";
import msg from "@/assets/tips";
import url from "@/assets/server";
import Qs from "qs";
export default {
  name: "articlepage",
  data() {
    return {
      user: {
        role: 0
      },
      category: [],
      filter: "",
      select: 5,
      art_data: [],
      article: [],
      article_show: [],
      selectCate: "全部",
      thisPage: 0,
      num: 0
    };
  },
  methods: {
    editArt(val, editor) {
      switch (editor) {
        case "ckeditor":
          if (confirm("该文章由 CKEditor 编写,是否使用 CKEditor 编辑?")) {
            document.getElementById("art_id1").value = val.$oid;
            document.getElementById("go1").submit();
          } else {
            this.$router.push({
              path: "/admin/newart",
              query: { id: val.$oid }
            });
          }
          break;
        case "wangeditor":
          if (confirm("该文章由 wangEditor 编写,是否使用 wangEditor 编辑?")) {
            document.getElementById("art_id2").value = val.$oid;
            document.getElementById("go2").submit();
          } else {
            this.$router.push({
              path: "/admin/newart",
              query: { id: val.$oid }
            });
          }
          break;
        default:
          this.$router.push({ path: "/admin/newart", query: { id: val.$oid } });
          break;
      }
    },
    delArt(val) {
      let self = this;
      this.axios
        .delete(url + "/api/article/", {
          data: Qs.stringify({
            _id: val.$oid
          })
        })
        .then(response => {
          if (response.data.code === 200) {
            for (let i = 0; i < this.art_data.length; i++) {
              if (this.art_data[i]._id.$oid == val.$oid) {
                this.art_data.splice(i, 1);
              }
            }
            self.search();
            msg(self.$t("lang.article.delsuccess"), "#2ecc71");
          } else {
            msg(self.$t("lang.article.delfail"), "red");
          }
        })
        .catch(response => {
          console.log(response);
        });
    },
    changePage(val) {
      this.thisPage = val - 1;
    },
    prev() {
      if (this.thisPage > 0) {
        this.thisPage--;
      }
    },
    next() {
      if (this.thisPage < this.num - 1) {
        this.thisPage++;
      }
    },
    paging(val) {
      this.num = Math.ceil(this.article.length / this.select);
      this.article_show = [];
      let arr = [];
      let j = 0;
      for (let i = 0; i < this.article.length; i++) {
        arr.push(this.article[i]);
        j++;
        if (j >= val) {
          this.article_show.push(arr);
          arr = [];
          j = 0;
        }
      }
      if (j != 0) {
        this.article_show.push(arr);
      }
      this.thisPage = 0;
    },
    search() {
      this.article = [];
      for (let i = 0; i < this.art_data.length; i++) {
        if (this.selectCate == "全部") {
          if (this.art_data[i].title.indexOf(this.filter) != -1) {
            this.article.push(this.art_data[i]);
          }
        } else {
          if (
            this.art_data[i].category_name == this.selectCate &&
            this.art_data[i].title.indexOf(this.filter) != -1
          ) {
            this.article.push(this.art_data[i]);
          }
        }
      }
      this.paging(this.select);
    }
  },
  mounted() {
    let load = loading(document.getElementById("table"));
    if (this.$store.state.user != null) {
      this.user = this.$store.state.user;
    } else {
      this.user = { role: 0 };
    }
    let self = this;
    this.axios
      .get(url + "/api/category/", {
        params: {
          user_id: self.user._id.$oid
        }
      })
      .then(response => {
        if (response.data.code === 200) {
          self.category = JSON.parse(response.data.data);
        } else {
          msg("未知错误..", "#FF9966");
          console.log(response.data);
        }
      })
      .catch(response => {
        msg("未知错误..", "#FF9966");
        console.log(response);
      });
    this.axios
      .get(url + "/api/article/", {
        params: {
          user_id: self.user._id.$oid
        }
      })
      .then(response => {
        if (response.data.code === 200) {
          self.article = JSON.parse(response.data.data);
          self.art_data = JSON.parse(response.data.data);
          self.paging(self.select);
          document.getElementById("table").removeChild(load);
        } else {
          msg("未知错误..", "#FF9966");
          console.log(response.data);
        }
      })
      .catch(response => {
        console.log(response);
      });
  },
  watch: {
    filter(val) {
      this.search();
    },
    selectCate(val) {
      this.search();
    },
    select(val) {
      this.paging(val);
    },
    num(val) {
      this.thisPage = 0;
    }
  }
};
</script>

<style lang="scss" scoped>
.prohibit_copy {
  -moz-user-select: none;
  -webkit-user-select: none;
  -ms-user-select: none;
  -khtml-user-select: none;
  user-select: none;
}
.articlepage {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 6px;
  padding: 10px 10px 30px 10px;
  box-sizing: border-box;
  .head {
    color: #fff;
    h5 {
      color: rgb(255, 59, 59);
    }
  }
  .fillter {
    height: 40px;
    width: 60%;
    margin-right: 1%;
    border: none;
    background: rgba(0, 0, 0, 0.2);
    outline: none;
    color: #fff;
    font-size: 18px;
    border-radius: 4px;
    padding-left: 15px;
    box-sizing: border-box;
  }
  .selectCate {
    height: 40px;
    width: 24%;
    margin-right: 1%;
    border: none;
    background: rgba(0, 0, 0, 0.2);
    outline: none;
    color: #fff;
    font-size: 18px;
    border-radius: 4px;
    padding-left: 10px;
    box-sizing: border-box;
  }
  .select {
    height: 40px;
    width: 14%;
    border: none;
    background: rgba(0, 0, 0, 0.2);
    outline: none;
    color: #fff;
    font-size: 18px;
    border-radius: 4px;
    padding-left: 10px;
    box-sizing: border-box;
  }
  .table {
    width: 100%;
    margin-top: 20px;
    .header {
      width: 100%;
      height: 50px;
      border-bottom: solid 2px #fff;
      transition: 0.4s;
      border-radius: 6px 6px 0 0;
      &:hover {
        background: rgba(0, 0, 0, 0.2);
      }
      span {
        height: 50px;
        line-height: 50px;
        font-size: 20px;
        color: #ddd;
        padding: 5px;
        box-sizing: border-box;
      }
      .col1 {
        display: inline-block;
        width: 20%;
        margin: 0 1%;
      }
      .col2 {
        display: inline-block;
        width: 32%;
        margin: 0 1%;
      }
      .col3 {
        display: inline-block;
        width: 20%;
        margin: 0 1%;
      }
      .col4 {
        display: inline-block;
        width: 20%;
        margin: 0 1%;
      }
    }
    .body {
      width: 100%;
      height: 35px;
      border-bottom: solid 1px #ddd;
      transition: 0.4s;
      border-radius: 6px 6px 0 0;
      margin-top: 10px;
      &:hover {
        background: rgba(0, 0, 0, 0.2);
      }
      span {
        height: 35px;
        line-height: 35px;
        font-size: 14px;
        color: #ddd;
        padding-left: 5px;
        box-sizing: border-box;
      }
      .col1 {
        display: inline-block;
        width: 20%;
        margin: 0 1%;
        overflow: hidden;
        font-weight: 600;
      }
      .red {
        color: rgb(255, 59, 59);
        font-weight: 600;
      }
      .col2 {
        display: inline-block;
        width: 32%;
        margin: 0 1%;
        overflow: hidden;
      }
      .col3 {
        display: inline-block;
        width: 20%;
        margin: 0 1%;
        overflow: hidden;
      }
      .col4 {
        display: inline-block;
        width: 20%;
        margin: 0 1%;
        overflow: hidden;
        button {
          background: rgba(255, 255, 255, 0.3);
          border: none;
          color: #fff;
          border-radius: 4px;
          height: 24px;
          transition: 0.4s;
          cursor: pointer;
          outline: none;
          width: 40%;
          &:hover {
            background: rgba(255, 255, 255, 0.5);
          }
        }
        .edit {
          margin-right: 16%;
        }
        .delete {
        }
      }
    }
    .msg {
      height: 50px;
      width: 100%;
      line-height: 50px;
      text-align: center;
      font-size: 35px;
      color: #ccc;
      margin-top: 20px;
    }
    .paging {
      width: 100%;
      height: 80px;
      margin-top: 20px;
      display: flex;
      justify-content: center;
      span {
        display: inline-block;
        height: 40px;
        width: 40px;
        margin: 20px 10px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transition: 0.4s;
        cursor: pointer;
        font-size: 20px;
        line-height: 43px;
        text-align: center;
        color: #ddd;
        &:hover {
          background: rgba(255, 255, 255, 0.5);
        }
        &:active {
          background: rgba(100, 100, 100, 0.2);
          color: #999;
        }
      }
    }
  }
}
</style>

