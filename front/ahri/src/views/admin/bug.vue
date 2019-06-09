<template>
  <div class="bug_manage">
    <h1>Bug</h1>
    <div class="item" v-for="i in bugs" :title="i.bug">
      <div class="date">{{i.date}}</div>
      <div class="username">{{i.username}}</div>
      <div class="bug_content">{{i.bug}}</div>
      <div class="opera">
        <button @click="del(i)">刪除</button>
      </div>
    </div>
  </div>
</template>

<script>
import Qs from "qs";
import msg from "@/assets/tips";
import url from "@/assets/server";
export default {
  name: "bug",
  data() {
    return {
      user: {
        role: 0
      },
      bugs: []
    };
  },
  methods: {
    del(val) {
      let self = this;
      this.axios
        .delete(url + "/api/bug/", {
          data: Qs.stringify({
            _id: val._id.$oid,
          })
        })
        .then(response => {
          if (response.data.code === 200) {
            for (let i = 0; i < this.bugs.length; i++) {
              if (this.bugs[i]._id == val._id) {
                this.bugs.splice(i, 1);
              }
            }
          } 
        })
        .catch(response => {
          console.log(response);
        });
    }
  },
  mounted() {
    if (this.$store.state.user != null) {
      this.user = this.$store.state.user;
    } else {
      this.user = { role: 0 };
    }
    let self = this;
    this.axios
      .get(url + "/api/bug/", {
        params: {
          user_id: self.user._id.$oid
        }
      })
      .then(response => {
        if (response.data.code === 200) {
          self.bugs = JSON.parse(response.data.data);
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
};
</script>

<style lang="scss" scoped>
.bug_manage {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 6px;
  padding: 10px;
  box-sizing: border-box;
  .item {
    display: flex;
    justify-content: space-between;
    margin: 5px;
    color: #ddd;
    overflow: hidden;
    background: rgba(0, 0, 0, 0.4);
    padding: 5px;
    cursor: pointer;
    transition: 0.4s;
    &:hover {
      background: rgba(0, 0, 0, 0.2);
    }
  }
  .date {
    width: 20%;
  }
  .username {
    width: 15%;
  }
  .bug_content {
    width: 50%;
  }
  .opera {
    width: 10%;
    button {
      background: rgba(255, 255, 255, 0.5);
      border: none;
      height: 24px;
      width: 80px;
      color: #fff;
      cursor: pointer;
      transition: 0.4s;
      outline: none;
      &:hover {
        background: rgba(255, 255, 255, 0.2);
      }
      &:active {
        background: rgba(0, 0, 0, 0.2);
      }
    }
  }
}
</style>
