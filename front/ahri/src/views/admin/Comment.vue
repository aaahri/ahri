<template>
  <div id="comment" class="comment">
    <div class="head prohibit_copy">
      <h3>{{$t('lang.comment.tab')}}</h3>
    </div>
    <select v-if="user.role == 100" class="selectCate" v-model:value="selectCate" name id>
      <option value="全部">{{$t('lang.comment.authors')}}</option>
      <option v-for="i in alluser" :value="i._id.$oid">{{i.username}}</option>
    </select>
    <input
      type="text"
      id="selectCate"
      class="selectCate"
      readonly
      v-if="user.role != 100"
      :value="user.username"
    >
    <input v-model:value="filter" class="fillter" type="text" placeholder="Filter . . .">
    <select class="select" v-model:value="select" name id>
      <option value="5">5</option>
      <option value="10">10</option>
      <option value="15">15</option>
      <option value="20">20</option>
      <option value="25">25</option>
    </select>
    <div class="table">
      <div class="header prohibit_copy">
        <span class="col1">User</span>
        <span class="col2">Content</span>
        <span class="col3">Article</span>
        <span class="col4">Date</span>
        <span class="col5">Opera</span>
      </div>
      <div v-for="i in comment_show[thisPage]" class="body">
        <span class="col1">{{i.user_name}}</span>
        <span class="col2">{{i.content}}</span>
        <span class="col3">{{i.art_title}}</span>
        <span class="col4">{{i.date}}</span>
        <span class="col5">
          <button class="delete" @click="delComment(i._id)">{{$t('lang.comment.delete')}}</button>
        </span>
      </div>
      <div class="msg" v-if="comment.length == 0">{{$t('lang.comment.msg')}}</div>
      <div class="paging" v-if="num > 1">
        <span class="prev iconfont ahriLeft-" @click="prev"></span>
        <span v-for="i in num" @click="changePage(i)">{{i}}</span>
        <span class="next iconfont ahriRight-" @click="next"></span>
      </div>
    </div>
  </div>
</template>

<script>
import Qs from "qs";
import loading from "@/assets/loading";
import url from "@/assets/server";
import msg from "@/assets/tips";
export default {
  name: "comment",
  data() {
    return {
      user: {
        role: 0
      },
      alluser: [],
      filter: "",
      select: 5,
      com_data: [],
      comment: [],
      comment_show: [],
      selectCate: "全部",
      thisPage: 0,
      num: 0
    };
  },
  methods: {
    delComment(val) {
      let self = this;
      this.axios
        .delete(url + "/api/comment_manage/", {
          data: Qs.stringify({
            _id: val.$oid
          })
        })
        .then(response => {
          if (response.data.code === 200) {
            for (let i = 0; i < this.com_data.length; i++) {
              if (this.com_data[i]._id.$oid == val.$oid) {
                this.com_data.splice(i, 1);
              }
            }
            self.search();
          } else {
            alert("failed");
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
      this.num = Math.ceil(this.comment.length / this.select);
      this.comment_show = [];
      let arr = [];
      let j = 0;
      for (let i = 0; i < this.comment.length; i++) {
        arr.push(this.comment[i]);
        j++;
        if (j >= val) {
          this.comment_show.push(arr);
          arr = [];
          j = 0;
        }
      }
      if (j != 0) {
        this.comment_show.push(arr);
      }
      this.thisPage = 0;
    },
    search() {
      this.comment = [];
      for (let i = 0; i < this.com_data.length; i++) {
        if (this.selectCate == "全部") {
          if (this.com_data[i].content.indexOf(this.filter) != -1) {
            this.comment.push(this.com_data[i]);
          }
        } else {
          if (
            this.com_data[i].author.$oid == this.selectCate &&
            this.com_data[i].content.indexOf(this.filter) != -1
          ) {
            this.comment.push(this.com_data[i]);
          }
        }
      }
      this.paging(this.select);
    }
  },
  mounted() {
    let load = loading(document.getElementById("comment"));
    if (this.$store.state.user != null) {
      this.user = this.$store.state.user;
    } else {
      this.user = { role: 0 };
    }
    let self = this;
    this.axios
      .get(url + "/api/comment_manage/", {
        params: {
          user_id: self.user._id.$oid
        }
      })
      .then(response => {
        if (response.data.code === 200) {
          self.comment = JSON.parse(response.data.data);
          self.com_data = JSON.parse(response.data.data);
          self.paging(self.select);
          document.getElementById("comment").removeChild(load);
        } else {
          msg("未知错误..", "#FF9966");
          console.log(response.data);
        }
      })
      .catch(response => {
        msg("未知错误..", "#FF9966");
        console.log(response);
      });
    if (localStorage.getItem("auth") != null) {
      this.user = JSON.parse(
        JSON.parse(localStorage.getItem("auth")).user.data
      );
      if (this.user.role == 100) {
        this.axios
          .get(url + "/api/auth/", {
            params: {
              user: self.user
            }
          })
          .then(response => {
            if (response.data.code === 200) {
              self.alluser = JSON.parse(response.data.data);
            } else {
              alert("failed");
            }
          })
          .catch(response => {
            console.log(response);
          });
      }
    } else {
      this.user = { role: 0 };
    }
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
.comment {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 6px;
  padding: 10px 10px 30px 10px;
  box-sizing: border-box;
  .head {
    color: #fff;
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
  #selectCate {
    cursor: pointer;
    text-align: right;
    padding-right: 20px;
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
        width: 12%;
        margin: 0 1%;
      }
      .col2 {
        display: inline-block;
        width: 40%;
        margin: 0 1%;
      }
      .col3 {
        display: inline-block;
        width: 16%;
        margin: 0 1%;
      }
      .col4 {
        display: inline-block;
        width: 11%;
        margin: 0 1%;
      }
      .col5 {
        display: inline-block;
        width: 10%;
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
        width: 12%;
        margin: 0 1%;
        overflow: hidden;
      }
      .col2 {
        display: inline-block;
        width: 40%;
        margin: 0 1%;
        overflow: hidden;
      }
      .col3 {
        display: inline-block;
        width: 16%;
        margin: 0 1%;
        overflow: hidden;
      }
      .col4 {
        display: inline-block;
        width: 11%;
        margin: 0 1%;
        overflow: hidden;
      }
      .col5 {
        display: inline-block;
        width: 10%;
        margin: 0 1%;
        overflow: hidden;
        button {
          background: rgba(255, 255, 255, 0.3);
          border: none;
          color: #fff;
          border-radius: 4px;
          height: 22px;
          transition: 0.4s;
          cursor: pointer;
          outline: none;
          width: 80%;
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

