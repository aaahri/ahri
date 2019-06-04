<template>
  <div id="usermanage" class="usermanage">
    <input class="filter" type="text" v-model="filter" :placeholder="$t('lang.usermanage.search')">
    <div class="item" v-for="i in users" v-if="!i.show">
      <div class="avatar">
        <img :src="i.avatar">
      </div>
      <div class="username">
        <span>{{$t('lang.usermanage.username')}} :</span>
        {{i.username}}
      </div>
      <div class="description">
        <span>{{$t('lang.usermanage.description')}} :</span>
        {{i.description}}
      </div>
      <div class="fullname">
        <span>{{$t('lang.usermanage.fullname')}} :</span>
        {{i.fullname}}
      </div>
      <div class="sex">
        <span>{{$t('lang.usermanage.sex')}} :</span>
        {{i.sex}}
      </div>
      <div class="birthday">
        <span>{{$t('lang.usermanage.birthday')}} :</span>
        {{i.birthday}}
      </div>
      <div class="last">
        <span>{{$t('lang.usermanage.last')}} :</span>
        {{i.last}}
      </div>
      <div class="email">
        <span>{{$t('lang.usermanage.email')}} :</span>
        {{i.email}}
      </div>
      <div class="telephone">
        <span>{{$t('lang.usermanage.telephone')}} :</span>
        {{i.telephone}}
      </div>
      <div class="join_date">
        <span>{{$t('lang.usermanage.join_date')}} :</span>
        {{i.join_date}}
      </div>
      <div class="level">
        <span>{{$t('lang.usermanage.level')}} :</span>
        {{i.level}}
      </div>
      <div v-if="i.disable" class="state">
        <span>{{$t('lang.usermanage.state')}} :</span>
        {{$t('lang.usermanage.disable')}}
      </div>
      <div v-if="!i.disable" class="state">
        <span>{{$t('lang.usermanage.state')}} :</span>
        {{$t('lang.usermanage.enable')}}
      </div>
      <div v-if="i.role != 100" class="disable">
        <button v-if="i.disable" @click="disable(i)">{{$t('lang.usermanage.enable')}}</button>
        <button v-if="!i.disable" @click="disable(i)">{{$t('lang.usermanage.disable')}}</button>
      </div>
      <div v-if="i.role != 100" class="delete">
        <button @click="delete_(i)">{{$t('lang.usermanage.delete')}}</button>
      </div>
      <div v-if="i.role != 100" class="role">
        <input type="text" name="role" v-model="i.role">
        <button @click="change_role(i)">{{$t('lang.usermanage.role')}}</button>
      </div>
    </div>
  </div>
</template>

<script>
import url from "@/assets/server";
import Qs from "qs";
import loading from "@/assets/loading";
import msg from "@/assets/tips";
export default {
  name: "usermanage",
  data() {
    return {
      user: {
        _id: {
          $oid: ""
        },
        role: 0
      },
      users: [],
      filter: ""
    };
  },
  methods: {
    change_role(val) {
      let self = this;
      this.axios
        .put(
          url + "/api/auth/usermanage/",
          Qs.stringify({
            id: self.user._id.$oid,
            user_id: val._id.$oid,
            role: val.role
          })
        )
        .then(response => {
          if (response.data.code === 200) {
            msg(self.$t("lang.usermanage.roleSuccess"), "#2ecc71");
          } else if (response.data.code === 400) {
            msg(this.$t("lang.usermanage.authFail"), "red");
          } else {
            msg("未知错误..(from usermanage put 500)", "#FF9966");
            console.log(response.data);
          }
        })
        .catch(response => {
          msg("未知错误..(from usermanage put)", "#FF9966");
          console.log(response);
        });
    },
    delete_(val) {
      let self = this;
      this.axios
        .delete(url + "/api/auth/usermanage/", {
          data: Qs.stringify({
            id: self.user._id.$oid,
            user_id: val._id.$oid
          })
        })
        .then(response => {
          if (response.data.code === 200) {
            self.users = JSON.parse(response.data.data);
            msg(self.$t("lang.usermanage.delsuccess"), "#82caa0");
          } else if (response.data.code === 400) {
            msg(self.$t("lang.usermanage.authFail"), "red");
            console.log(response.data);
          } else {
            msg("未知错误..(from usermanage del)", "#FF9966");
            console.log(response.data);
          }
        })
        .catch(response => {
          msg("未知错误..", "#FF9966");
          console.log(response);
        });
    },
    disable(val) {
      let self = this;
      this.axios({
        url: url + "/api/auth/usermanage/",
        method: "post",
        data: JSON.stringify({
          id: self.user._id.$oid,
          user_id: val._id.$oid,
          disable: !val.disable
        }),
        headers: {
          "Content-Type": "application/json"
        }
      }).then(
        function(response) {
          if (response.data.code === 200) {
            self.users = JSON.parse(response.data.data);
            msg(self.$t("lang.usermanage.userSuccess"), "#2ecc71");
          } else if (response.data.code === 400) {
            msg(self.$t("lang.usermanage.authFail"), "red");
          } else {
            msg("未知错误..(from usermanage post)", "#FF9966");
            console.log(response.data);
          }
        },
        function(response) {
          msg("未知错误..", "#FF9966");
          console.log(response);
        }
      );
    }
  },
  mounted() {
    let load = loading(document.getElementById("usermanage"));
    if (this.$store.state.user != null) {
      this.user = this.$store.state.user;
    } else {
      this.user = { role: 0 };
    }
    let self = this;
    this.axios
      .get(url + "/api/auth/usermanage/", {
        params: {
          user: self.user
        }
      })
      .then(response => {
        if (response.data.code === 200) {
          self.users = JSON.parse(response.data.data);
          document.getElementById("usermanage").removeChild(load);
        } else if (response.data.code === 400) {
          msg(this.$t("lang.usermanage.userfail"), "red");
        } else {
          msg("未知错误..(from usermanage get)", "#FF9966");
          console.log(response.data);
        }
      })
      .catch(response => {
        msg("未知错误..", "#FF9966");
        console.log(response);
      });
  },
  watch: {
    filter(val) {
      for (let i = 0; i < this.users.length; i++) {
        if (this.users[i].username.indexOf(val) == -1) {
          this.users[i].show = true;
        } else {
          this.users[i].show = false;
        }
      }
    }
  }
};
</script>

<style lang="scss" scoped>
.usermanage {
  background: rgba(0, 0, 0, 0.3);
  height: 100%;
  padding: 15px;
  box-sizing: border-box;
  border-radius: 4px;
  position: relative;
  .filter {
    width: 100%;
    height: 40px;
    font-size: 22px;
    border-radius: 6px;
    border: none;
    background: rgba(0, 0, 0, 0.6);
    outline: none;
    color: #fff;
    padding: 0 15px;
    box-sizing: border-box;
  }
  .item {
    position: relative;
    width: 100%;
    height: 130px;
    background: rgba(0, 0, 0, 0.5);
    margin: 15px;
    div {
      color: #ccc;
      height: 26px;
      overflow: hidden;
      width: 240px;
      overflow: hidden;
      span {
        font-size: 18px;
        color: #fff;
        margin-right: 10px;
      }
    }
    .avatar {
      position: absolute;
      top: 15px;
      left: 10px;
      height: 100px;
      img {
        height: 100px;
      }
    }
    .username {
      position: absolute;
      top: 10px;
      left: 130px;
    }
    .description {
      position: absolute;
      top: 10px;
      left: 380px;
    }
    .fullname {
      position: absolute;
      top: 40px;
      left: 130px;
    }
    .sex {
      position: absolute;
      top: 40px;
      left: 380px;
    }
    .birthday {
      position: absolute;
      top: 40px;
      left: 630px;
    }
    .email {
      position: absolute;
      top: 70px;
      left: 130px;
    }
    .telephone {
      position: absolute;
      top: 70px;
      left: 380px;
    }
    .last {
      position: absolute;
      top: 70px;
      left: 630px;
    }
    .join_date {
      position: absolute;
      top: 100px;
      left: 130px;
    }
    .level {
      position: absolute;
      top: 100px;
      left: 380px;
    }
    .state {
      position: absolute;
      top: 100px;
      left: 630px;
    }
    .disable {
      position: absolute;
      top: 10px;
      left: 880px;
      button {
        background: rgba(255, 255, 255, 0.4);
        border: none;
        width: 127px;
        height: 26px;
        color: #fff;
        border-radius: 4px;
        outline: none;
        transition: 0.4s;
        cursor: pointer;
        &:hover {
          background: rgba(255, 255, 255, 0.2);
        }
      }
    }
    .delete {
      position: absolute;
      top: 50px;
      left: 880px;
      button {
        background: rgba(255, 255, 255, 0.4);
        border: none;
        width: 127px;
        height: 26px;
        color: red;
        border-radius: 4px;
        outline: none;
        transition: 0.4s;
        cursor: pointer;
        &:hover {
          background: rgba(255, 255, 255, 0.2);
        }
      }
    }
    .role {
      position: absolute;
      top: 90px;
      left: 880px;
      input {
        background: rgba(0, 0, 0, 0.4);
        border: none;
        width: 40px;
        height: 20px;
        color: #fff;
        border-radius: 4px;
        outline: none;
        border: solid 1px #fff;
        margin-right: 5px;
      }
      button {
        background: rgba(255, 255, 255, 0.4);
        border: none;
        width: 80px;
        height: 26px;
        color: #fff;
        border-radius: 4px;
        outline: none;
        transition: 0.4s;
        cursor: pointer;
        &:hover {
          background: rgba(255, 255, 255, 0.2);
        }
      }
    }
  }
}
</style>
