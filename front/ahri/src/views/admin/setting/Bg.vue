<template>
  <div class="bg">
    <div class="item" v-for="i in bgs">
      <div class="mask" v-if="i.username">
        <span>{{i.username}}</span>
        <button @click="del(i)">{{$t('lang.setting.bgs.del')}}</button>
      </div>
      <div class="mask" v-else>
        <span>{{$t('lang.setting.bgs.sys')}}</span>
      </div>
      <img :src="i.url" alt>
    </div>
    <div class="item">
      <label for="upload" class="add">＋</label>
      <input type="file" @change="upload()" id="upload" hidden ref="upload">
    </div>
  </div>
</template>

<script>
import url from "@/assets/server";
import Qs from "qs";
import msg from "@/assets/tips";
export default {
  name: "bg",
  data() {
    return {
      bgs: [],
      user: { username: "", role: 0 }
    };
  },
  created() {
    if (this.$store.state.user != null) {
      this.user = this.$store.state.user;
    } else {
      this.user = { role: 0 };
    }
  },
  methods: {
    del(val) {
      let self = this;
      this.axios
        .delete(url + "/api/bg_setting/", {
          data: Qs.stringify({
            _id: val._id.$oid
          })
        })
        .then(response => {
          if (response.data.code === 200) {
            for (let i = 0; i < this.bgs.length; i++) {
              if (this.bgs[i]._id == val._id) {
                this.bgs.splice(i, 1);
              }
            }
          } else {
            msg("未知错误..", "#FF9966");
            console.log(response.data);
          }
        })
        .catch(response => {
          msg("未知错误..", "#FF9966");
          console.log(response);
        });
    },
    upload() {
      let self = this;
      let formData = new FormData();
      formData.append("bg", this.$refs.upload.files[0]);
      formData.append("username", self.user.username);
      formData.append("user_id", self.user._id.$oid);
      const instance = this.axios.create({
        withCredentials: true
      });
      instance.post(url + "/api/bg_setting/", formData).then(response => {
        if (response.data.code === 200) {
          this.bgs.push(JSON.parse(response.data.data));
        } else {
          msg(self.$t("lang.category.uploadfail"), "red");
        }
      });
    }
  },
  mounted() {
    let self = this;
    this.axios
      .get(url + "/api/bg_setting/", {
        params: {
          bg: "ma",
          user_id: self.$store.state.user._id.$oid
        }
      })
      .then(response => {
        if (response.data.code === 200) {
          self.bgs = JSON.parse(response.data.data);
        } else {
          console.log(response.data);
        }
      })
      .catch(response => {
        console.log(response);
      });
  }
};
</script>

<style lang="scss" scoped>
.bg {
  background: rgba(0,0,0,.5);
  .item {
    position: relative;
    margin: 15px;
    float: left;
    width: 160px;
    height: 90px;
    background: rgba(255, 255, 255, 0.3);
    border-radius: 6px;
    transition: 0.4s;
    &:hover {
      background: rgba(255, 255, 255, 0.1);
    }
    .mask {
      position: absolute;
      width: 100%;
      height: 0;
      top: 0;
      left: 0;
      background: rgba(0, 0, 0, 0.6);
      transition: 0.5s;
      text-align: center;
      cursor: pointer;
      overflow: hidden;
      color: #fff;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      span {
        width: 100px;
        overflow: hidden;
        margin-bottom: 15px;
      }
      button {
        background: rgba(255, 255, 255, 0.2);
        border: none;
        border-radius: 4px;
        height: 26px;
        width: 70px;
        color: #fff;
        cursor: pointer;
        transition: 0.4s;
        &:hover {
          background: rgba(0, 0, 0, 0.5);
        }
      }
    }
    .add {
      display: block;
      width: 100%;
      height: 100%;
      font-size: 40px;
      line-height: 90px;
      color: #fff;
      cursor: pointer;
      text-align: center;
    }
    img {
      height: 90px;
      width: 160px;
    }
    &:hover > .mask {
      height: 90px;
    }
  }
}
</style>
