<template>
  <div id="app">
    <div class="bug">
      <div class="bug_msg">
        <textarea name v-model="bug"></textarea>
        <button @click="send">Send</button>
      </div>
      <div class="bug_btn" @click="show"></div>
    </div>
    <router-view/>
  </div>
</template>

<script>
import url from "@/assets/server";
export default {
  name: "app",
  data() {
    return {
      user: { role: 0, _id: { $oid: "" } },
      is_show: false,
      bug: ""
    };
  },
  methods: {
    show() {
      let bug = document.getElementsByClassName("bug")[0];
      if (this.is_show) {
        bug.style.width = "40px";
        bug.style.height = "40px";
        this.is_show = false;
      } else {
        bug.style.width = "380px";
        bug.style.height = "220px";
        this.is_show = true;
      }
    },
    send() {
      let bug = document.getElementsByClassName("bug")[0];
      let self = this;
        this.axios({
          url: url + "/api/bug/",
          method: "post",
          //发送格式为json
          data: JSON.stringify({
            user_id: self.user._id.$oid,
            bug:self.bug
          }),
          headers: {
            "Content-Type": "application/json"
          }
        }).then(
          function(response) {
          },
          function(response) {
            console.log(response);
          }
        );
      alert("感谢！");
      this.bug = "";
      bug.style.width = "40px";
      bug.style.height = "40px";
      this.is_show = false;
    }
  },
  mounted() {
    if (this.$store.state.user != null) {
      this.user = this.$store.state.user;
    } else {
      this.user = { role: 0, _id: { $oid: "" } };
    }
  }
};
</script>

<style lang="scss">
html,
body {
  padding: 0;
  margin: 0;
  width: 100%;
  height: 100%;
}
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  // text-align: center;
  color: #2c3e50;
  height: 100%;
  .bug {
    z-index: 999999999;
    width: 40px;
    height: 40px;
    background: rgba(0, 0, 0, 0.3);
    position: fixed;
    right: 0;
    bottom: 0;
    overflow: hidden;
    transition: 0.5s;
    // &:hover {
    //   width: 380px;
    //   height: 220px;
    // }
    .bug_btn {
      width: 40px;
      height: 40px;
      background: rgba(0, 0, 0, 0.3);
      position: absolute;
      right: 0;
      bottom: 0;
      transition: 1s;
      cursor: pointer;
    }
    .bug_msg {
      textarea {
        width: 300px;
        height: 140px;
        margin: 10px 40px;
        resize: none;
        font-size: 18px;
        color: #2c3e50;
        padding: 10px;
        font-weight: 600;
      }
      button {
        float: right;
        margin: 0 140px;
        width: 100px;
        height: 35px;
      }
    }
  }
}
// #nav {
//   padding: 30px;
//   a {
//     font-weight: bold;
//     color: #2c3e50;
//     &.router-link-exact-active {
//       color: #42b983;
//     }
//   }
// }
</style>
