<template>
  <div id="category" class="category">
    <div class="head prohibit_copy">
      <h3>{{$t('lang.category.tab')}}</h3>
    </div>
    <transition name="fade">
      <div v-if="show" class="mask">
        <div class="popup">
          <div class="close prohibit_copy" @click="show = false">×</div>
          <div class="edit_area">
            <input
              class="name"
              v-model:value="edit_area.name"
              type="text"
              :placeholder="$t('lang.category.title')"
            >
            <textarea
              class="desc"
              v-model:value="edit_area.desc"
              rows="4"
              :placeholder="$t('lang.category.desc')"
            ></textarea>
            <input
              class="thumbnail"
              v-model:value="edit_area.thumbnail"
              type="text"
              :placeholder="$t('lang.category.thumbnail')"
            >
            <label for="upload_input" class="upload prohibit_copy">{{$t('lang.category.upload')}}</label>
            <input id="upload_input" @change="upload()" ref="upload" hidden type="file">
            <div class="private">
              <input
                hidden
                v-model:value="edit_area.private"
                type="checkbox"
                id="toggle-button"
                name="switch"
              >
              <label for="toggle-button" class="button-label prohibit_copy">
                <span class="circle"></span>
                <span class="text on">{{$t('lang.category.private')}}</span>
                <span class="text off">{{$t('lang.category.public')}}</span>
              </label>
            </div>
            <button class="submit prohibit_copy" @click="submit">{{$t('lang.category.submit')}}</button>
          </div>
        </div>
      </div>
    </transition>
    <div class="container">
      <div id="center" class="center">
        <input
          class="filter"
          v-model:value="filter"
          type="text"
          :placeholder="$t('lang.category.fillter')"
        >
        <div v-for="i in category" v-if="!i.show" :class="{ 'item': true, 'pri_cate': i.private}">
          <div class="thumbnail prohibit_copy">
            <img :src="i.thumbnail" alt>
          </div>
          <div class="info">
            <div class="name">{{i.name}}</div>
            <div class="author">By {{i.author_name}} @ {{i.change_date}}</div>
            <div class="desc">{{i.desc}}</div>
            <div class="opera">
              <button class="prohibit_copy" @click="edit(i)">{{$t('lang.category.edit')}}</button>
              <button class="prohibit_copy" @click="del(i)">{{$t('lang.category.delete')}}</button>
            </div>
          </div>
        </div>
        <div class="item add" @click="add()">+</div>
      </div>
    </div>
  </div>
</template>

<script>
import msg from "@/assets/tips";
import loading from "@/assets/loading";
import url from "@/assets/server";
import Qs from "qs";
export default {
  name: "category",
  data() {
    return {
      user: {
        role: 0
      },
      show: false,
      is_edit: false,
      filter: "",
      edit_area: {
        id: 0,
        name: "Title",
        thumbnail: url + "/static/ahri.jpg",
        desc: "../../assets/ahri.jpg",
        author: "ahri",
        date: "2019-05-09",
        private: false
      },
      category: []
    };
  },
  methods: {
    upload() {
      let self = this;
      let formData = new FormData();
      formData.append("thumbnail", this.$refs.upload.files[0]);
      formData.append("username", self.user.username);
      const instance = this.axios.create({
        withCredentials: true
      });
      instance.post(url + "/api/category/upload/", formData).then(response => {
        if (response.data.code === 200) {
          self.edit_area.thumbnail = response.data.url;
        } else {
          msg(self.$t("lang.category.uploadfail"), "red");
        }
      });
    },
    edit(val) {
      this.is_edit = true;
      this.cache = val;
      this.edit_area = val;
      this.show = true;
    },
    del(val) {
      let self = this;
      this.axios
        .delete(url + "/api/category/", {
          data: Qs.stringify({
            _id: val._id.$oid,
            user_id: self.user._id.$oid,
            author: val.author_name
          })
        })
        .then(response => {
          if (response.data.code === 200) {
            for (let i = 0; i < this.category.length; i++) {
              if (this.category[i]._id == val._id) {
                this.category.splice(i, 1);
              }
            }
            msg(self.$t("lang.category.delsuccess"), "#82caa0");
          } else if (response.data.code === 400) {
            msg(self.$t("lang.category.notNull"), "red");
            console.log(response.data);
          } else {
            msg("未知错误..(from category del 500)", "#FF9966");
            console.log(response.data);
          }
        })
        .catch(response => {
          msg("未知错误..(from category del)", "#FF9966");
          console.log(response);
        });
    },
    add() {
      this.is_edit = false;
      this.edit_area = {
        name: "",
        thumbnail: url + "/static/ahri.jpg",
        desc: "",
        author: this.user._id.$oid,
        date: "",
        private: false
      };
      this.show = true;
    },
    submit() {
      if (this.edit_area.name == "") {
        msg(this.$t("lang.category.nameNull"), "red");
        return false;
      }
      if (this.is_edit) {
        //编辑
        let self = this;
        this.axios
          .put(
            url + "/api/category/",
            Qs.stringify({
              category: JSON.stringify(self.edit_area),
              user: JSON.stringify(self.user)
            })
          )
          .then(response => {
            if (response.data.code === 200) {
              this.show = false;
              for (let i = 0; i < this.category.length; i++) {
                if (i.id == this.edit_area.id) {
                  i = this.edit_area;
                }
              }
              msg(self.$t("lang.category.editsuccess"), "#2ecc71");
            } else if (response.data.code === 400) {
              msg(this.$t("lang.category.authFail"), "red");
            } else if (response.data.code === 401) {
              msg(this.$t("lang.category.nameHas"), "red");
            } else {
              msg("未知错误..(from category put 500)", "#FF9966");
              console.log(response.data);
            }
          })
          .catch(response => {
            msg("未知错误..(from category put)", "#FF9966");
            console.log(response);
          });
      } else {
        //新加
        let self = this;
        this.axios({
          url: url + "/api/category/",
          method: "post",
          //发送格式为json
          data: JSON.stringify({
            form: self.edit_area,
            user: self.user
          }),
          headers: {
            "Content-Type": "application/json"
          }
        }).then(
          function(response) {
            if (response.data.code === 200) {
              self.category.push(JSON.parse(response.data.data));
              msg(self.$t("lang.category.addsuccess"), "#2ecc71");
              self.show = false;
            } else if (response.data.code === 400) {
              msg(self.$t("lang.category.authFail"), "red");
            } else if (response.data.code === 401) {
              msg(self.$t("lang.category.nameHas"), "red");
            } else {
              msg("未知错误..(from category post 500)", "#FF9966");
              console.log(response.data);
            }
          },
          function(response) {
            msg("未知错误..(from category post)", "#FF9966");
            console.log(response);
          }
        );
      }
    }
  },
  mounted() {
    let load = loading(document.getElementById("center"));
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
          document.getElementById("center").removeChild(load);
        } else if (response.data.code === 400) {
          msg(this.$t("lang.category.authFail"), "red");
        } else {
          msg("未知错误..(from category get 500)", "#FF9966");
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
      for (let i = 0; i < this.category.length; i++) {
        if (this.category[i].name.indexOf(val) == -1) {
          this.category[i].show = true;
        } else {
          this.category[i].show = false;
        }
      }
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
.private {
  margin: 12px 0 0 24px;
  float: left;
  .button-label {
    position: relative;
    display: inline-block;
    width: 110px;
    height: 30px;
    background-color: rgba(0, 0, 0, 0.4);
    box-shadow: #ccc 0px 0px 0px 2px;
    border-radius: 15px;
    overflow: hidden;
    cursor: pointer;
    &:hover > .circle {
      background-color: rgba(255, 255, 255, 0.8);
    }
    .circle {
      position: absolute;
      top: 0;
      left: 0;
      width: 30px;
      height: 30px;
      border-radius: 50%;
      background-color: rgba(255, 255, 255, 0.6);
    }
    .text {
      line-height: 30px;
      font-size: 18px;
      text-shadow: 0 0 2px #ddd;
    }

    .on {
      color: #fff;
      display: none;
      text-indent: 10px;
    }
    .off {
      color: #fff;
      display: inline-block;
      text-indent: 34px;
    }
    .circle {
      left: 0;
      transition: all 0.3s;
    }
  }
}

#toggle-button:checked + label.button-label .circle {
  left: 80px;
}
#toggle-button:checked + label.button-label .on {
  display: inline-block;
}
#toggle-button:checked + label.button-label .off {
  display: none;
}
#toggle-button:checked + label.button-label {
  background-color: rgba(255, 255, 255, 0.3);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
.mask {
  z-index: 300;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.3);
  .popup {
    position: absolute;
    top: 50%;
    left: 50%;
    height: 420px;
    width: 600px;
    margin-top: -210px;
    margin-left: -300px;
    background: rgba(0, 0, 0, 0.9);
    border-radius: 8px;
    .close {
      float: right;
      margin: 5px 10px 0 0;
      height: 30px;
      width: 30px;
      line-height: 30px;
      text-align: center;
      border-radius: 50%;
      font-size: 20px;
      background: #333;
      color: #ccc;
      cursor: pointer;
      transition: 0.3s;
      &:hover {
        font-size: 30px;
        background: #3336;
        color: #aaa;
        transform: rotate(180deg);
        -ms-transform: rotate(180deg); /* IE 9 */
        -moz-transform: rotate(180deg); /* Firefox */
        -webkit-transform: rotate(180deg); /* Safari 和 Chrome */
        -o-transform: rotate(180deg);
      }
    }
    .edit_area {
      margin-top: 50px;
      .name {
        width: 90%;
        margin: 10px 4%;
        border: none;
        background: none;
        outline: none;
        border-bottom: solid 1px #ddd;
        font-size: 22px;
        color: #fff;
        padding: 4px;
      }
      .desc {
        width: 90%;
        margin: 10px 4%;
        border: none;
        background: none;
        outline: none;
        resize: none;
        border-bottom: solid 1px #ddd;
        font-size: 22px;
        color: #fff;
        padding: 4px;
      }
      .thumbnail {
        width: 70%;
        margin: 10px 0 10px 4%;
        border: none;
        background: none;
        outline: none;
        border-bottom: solid 1px #ddd;
        font-size: 22px;
        color: #fff;
        padding: 4px;
      }
      .upload {
        display: inline-block;
        width: 18%;
        margin: 10px 4% 10px 10px;
        border: none;
        height: 35px;
        line-height: 35px;
        text-align: center;
        background: rgba(100, 100, 100, 0.3);
        outline: none;
        color: #fff;
        cursor: pointer;
        border-radius: 4px;
        transition: 0.3s;
        &:hover {
          background: rgba(200, 200, 200, 0.4);
        }
        &:active {
          background: rgba(150, 150, 150, 0.4);
        }
      }
      .submit {
        width: 30%;
        margin: 10px 4% 10px 65%;
        border: none;
        height: 38px;
        line-height: 38px;
        background: rgba(100, 100, 100, 0.3);
        outline: none;
        color: #fff;
        cursor: pointer;
        border-radius: 4px;
        transition: 0.3s;
        &:hover {
          background: rgba(200, 200, 200, 0.5);
        }
        &:active {
          background: rgba(150, 150, 150, 0.4);
        }
      }
    }
  }
}
.category {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 6px;
  padding: 10px;
  box-sizing: border-box;
  .head {
    color: #fff;
  }
  .container {
    color: #fff;
    display: flex;
    justify-content: center;
    .center {
      width: 500px;
      display: flex;
      flex-wrap: wrap;
      .filter {
        border: none;
        background: none;
        width: 100%;
        border-bottom: solid 1px #fff;
        font-size: 22px;
        padding: 5px;
        box-sizing: border-box;
        color: #fff;
        outline: none;
        margin-bottom: 10px;
      }
      .item {
        height: 140px;
        width: 480px;
        margin: 10px;
        border-radius: 6px;
        background: rgba(255, 255, 255, 0.2);
        transition: 0.5s;
        display: flex;
        justify-content: space-between;
        &:hover {
          background: rgba(255, 255, 255, 0.1);
        }
        .thumbnail {
          height: 140px;
          width: 140px;
          display: flex;
          justify-content: center;
          align-items: center;
          img {
            height: 100px;
            width: 100px;
          }
        }
        .info {
          padding: 5px;
          box-sizing: border-box;
          height: 140px;
          width: 360px;
          text-align: left;
          .name {
            font-size: 24px;
          }
          .author {
            font-size: 18px;
          }
          .desc {
            width: 340px;
            height: 42px;
            overflow: hidden;
            font-size: 14px;
          }
          .opera {
            button {
              height: 30px;
              width: 100px;
              margin: 0 10px;
              border: none;
              background: rgba(0, 0, 0, 0.5);
              color: #ddd;
              font-size: 16px;
              border-radius: 4px;
              transition: 0.5s;
              cursor: pointer;
              outline: none;
              &:hover {
                background: rgba(0, 0, 0, 0.8);
              }
              &:active {
                background: rgba(0, 0, 0, 0.4);
              }
            }
          }
        }
      }
      .pri_cate {
        background: rgba(0, 0, 0, 0.6);
        &:hover {
          background: rgba(0, 0, 0, 0.4);
        }
      }
      .add {
        background: rgba(255, 255, 255, 0.2);
        transition: 0.5s;
        cursor: pointer;
        font-size: 80px;
        color: #fff;
        display: flex;
        justify-content: center;
        align-items: center;
        &:active {
          background: rgba(0, 0, 0, 0.2);
        }
      }
    }
    @media screen and (min-width: 1330px) {
      .center {
        width: 1010px;
      }
    }
  }
}
</style>
