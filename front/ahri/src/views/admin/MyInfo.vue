<template>
  <div id="myinfo" class="myinfo">
    <div class="head prohibit_copy">
      <h3>{{$t('lang.myinfo.tab')}}</h3>
    </div>
    <div class="avatar prohibit_copy">
      <img :src="user.avatar" alt>
      <label for="upload">
        Upload
        <input @change="upload()" ref="upload" hidden type="file" id="upload">
      </label>
    </div>
    <div class="info">
      <div class="item username">
        <div class="tit prohibit_copy">username</div>
        <div class="con">{{user.username}}</div>
      </div>
      <div class="item email">
        <div class="tit prohibit_copy">email</div>
        <div class="con">{{user.email}}</div>
      </div>
      <div class="item fullname">
        <div class="tit prohibit_copy">fullname</div>
        <div class="con">
          <input type="text" v-model:value="user.fullname" placeholder="fullname">
        </div>
      </div>
      <div class="item description">
        <div class="tit prohibit_copy">description</div>
        <div class="con">
          <input type="text" v-model:value="user.description" placeholder="description">
        </div>
      </div>
      <div class="item telephone">
        <div class="tit prohibit_copy">telephone</div>
        <div class="con">
          <input type="text" v-model:value="user.telephone" placeholder="telephone">
        </div>
      </div>
      <div class="item sex">
        <div class="tit prohibit_copy">sex</div>
        <div class="con prohibit_copy">
          <label for>
            <input type="radio" name="sex" v-model="user.sex" value="男">{{$t('lang.myinfo.male')}}
          </label>
          <label for>
            <input type="radio" name="sex" v-model="user.sex" value="女">{{$t('lang.myinfo.female')}}
          </label>
          <label for>
            <input type="radio" name="sex" v-model="user.sex" value="不男不女">{{$t('lang.myinfo.secrecy')}}
          </label>
        </div>
      </div>
      <div class="item birthday">
        <div class="tit prohibit_copy">birthday</div>
        <div class="con">
          {{user.birthday}}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input id="date" type="date" v-model="user.birthday">
        </div>
      </div>
      <div class="item last">
        <div class="tit prohibit_copy">last_login</div>
        <div class="con">{{user.last}}</div>
      </div>
      <div class="item join_date">
        <div class="tit prohibit_copy">join_date</div>
        <div class="con">{{user.join_date}}</div>
      </div>
      <div class="item level">
        <div class="tit prohibit_copy">level</div>
        <div class="con">{{user.level}}</div>
      </div>
    </div>
    <div class="opera prohibit_copy">
      <button class="change" @click="change">Change</button>
    </div>
  </div>
</template>

<script>
import msg from "@/assets/tips";
import loading from "@/assets/loading";
import url from "@/assets/server";
import Qs from "qs";
export default {
  name: "myinfo",
  data() {
    return {
      user: {
        role: 0
      },
      sex: ""
    };
  },
  methods: {
    upload() {
      let self = this;
      let formData = new FormData();
      formData.append("avatar", this.$refs.upload.files[0]);
      formData.append("username", self.user.username);
      const instance = this.axios.create({
        withCredentials: true
      });
      instance.post(url + "/api/auth/upload/", formData).then(response => {
        if (response.data.code === 200) {
          self.user.avatar = response.data.url;
        } else {
          msg(self.$t("lang.myinfo.uploadFail"), "red");
        }
      });
    },
    change() {
      let self = this;
      this.axios
        .put(
          url + "/api/auth/",
          Qs.stringify({
            user: JSON.stringify(self.user)
          })
        )
        .then(response => {
          if (response.data.code === 200) {
            let auth = {
              user: response.data
            };
            self.$store.commit('SAVE_USER', auth);
            msg(self.$t("lang.myinfo.success"), "#2ecc71");
          } else {
            msg("未知错误..", "#FF9966");
            console.log(response.data);
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
  }
};
</script>

<style lang="scss" scoped>
.myinfo {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 6px;
  padding: 10px;
  box-sizing: border-box;
  .head {
    color: #fff;
  }
  .avatar {
    display: flex;
    justify-content: center;
    align-items: center;
    img {
      width: 120px;
      height: 120px;
    }
    label {
      margin: 0 0 0 50px;
      display: inline-block;
      height: 40px;
      width: 120px;
      border-radius: 4px;
      text-align: center;
      line-height: 40px;
      background: rgba(0, 0, 0, 0.6);
      color: #fff;
      cursor: pointer;
      transition: 0.3s;
      &:hover {
        background: rgba(255, 255, 255, 0.1);
      }
      &:active {
        background: rgba(0, 0, 0, 0.4);
      }
    }
  }
  .info {
    color: #fff;
    .item {
      margin: 20px;
      height: 30px;
      line-height: 30px;
      border-radius: 4px;
      background: rgba(0, 0, 0, 0.3);
      .tit {
        width: 200px;
        float: left;
        text-align: right;
        padding-right: 15px;
        border-right: solid 1px #ddd;
      }
      .con {
        padding-left: 15px;
        float: left;
        input[type="text"] {
          background: none;
          color: #fff;
          height: 30px;
          border: none;
          outline: none;
          width: 300px;
        }
        label {
          margin: 0 20px;
        }
      }
    }
    .email,
    .username,
    .last,
    .join_date,
    .level {
      .con {
        color: #2ecc71;
      }
    }
  }
  .opera {
    width: 100%;
    display: flex;
    justify-content: center;
    margin: 40px 0 100px 0;
    .change {
      width: 160px;
      height: 40px;
      background: rgba(255, 255, 255, 0.2);
      color: #fff;
      font-size: 20px;
      border: none;
      cursor: pointer;
      transition: 0.5s;
      border-radius: 2px;
      outline: none;
      &:hover {
        background: rgba(255, 255, 255, 0.4);
      }
      &:active {
        background: rgba(0, 0, 0, 0.6);
      }
    }
  }
}
</style>
