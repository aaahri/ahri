<template>
  <div id="newarticle" class="newarticle">
    <div class="title">{{$t('lang.newart.Ttitle1')}}:</div>
    <form id="go3" action="javascript:void(0)">
      <input type="submit" id="editor3" value="待续...">
    </form>
    <form id="go1" action="https://www.0x0001.com/editor/ckeditor/" method="post">
      <input hidden type="text" name="user" v-model:value="user._id.$oid">
      <input hidden type="text" name="type" value="n">
      <input type="submit" id="editor1" value="CKEditor">
    </form>
    <form id="go2" action="https://www.0x0001.com/editor/wangeditor/" method="post">
      <input hidden type="text" name="user" v-model:value="user._id.$oid">
      <input hidden type="text" name="type" value="n">
      <input type="submit" id="editor2" value="wangEditor">
    </form>
    <!-- <button @click="ckeditor">CKEditor</button> -->
    <input
      class="pla"
      v-model:value="article.title"
      type="text"
      name="title"
      :placeholder="$t('lang.newart.Ttitle1')"
      id
    >
    <select class="pla cate" v-model:value="article.category" name="cate" id>
      <option v-for="i in category" :value="i._id.$oid">{{i.name}}</option>
    </select>
    <div class="thumbnail">
      <input
        class="pla thumbnail"
        type="text"
        name="thumbnail"
        :placeholder="$t('lang.newart.thumbnail')"
        id
        v-model:value="article.thumbnail"
      >
      <label for="upload_input" class="upload prohibit_copy">{{$t('lang.newart.upload')}}</label>
      <input id="upload_input" @change="upload()" ref="upload" hidden type="file">
    </div>
    <textarea
      class="pla desc"
      v-model:value="article.desc"
      name
      id
      rows="4"
      :placeholder="$t('lang.newart.desc')"
    ></textarea>
    <!-- <iframe name="myFrame" width="100%" height="200px" style="border:none"></iframe> -->
    <quill-editor
      v-model="content"
      ref="myQuillEditor"
      :options="editorOption"
      @blur="onEditorBlur($event)"
      @focus="onEditorFocus($event)"
      @change="onEditorChange($event)"
    ></quill-editor>
    <br>
    <div class="opera">
      <button v-if="user.role == 100" @click="indexshow">{{$t('lang.newart.indexshow')}}</button>
      <button v-if="!newart" @click="change">{{$t('lang.newart.save')}}</button>
      <button @click="addart">{{$t('lang.newart.submit')}}</button>
    </div>
    <!-- <code v-html="content"></code> -->
  </div>
</template>

<script>
import Qs from "qs";
import loading from "@/assets/loading";
import url from "@/assets/server";
import msg from "@/assets/tips";
import "highlight.js/styles/vs2015.css";
import { quillRedefine } from "vue-quill-editor-upload";
import hljs from "highlight.js";
export default {
  name: "newarticle",
  data() {
    return {
      user: {
        _id: {
          $oid: ""
        },
        role: 0
      },
      category: [],
      article: {
        _id: "",
        title: "",
        desc: "",
        category: "",
        thumbnail: "",
        content: "",
        editor: "quill"
      },
      content: `<br><br><pre class="ql-syntax" spellcheck="false">printf('Hello, world!'); </pre> `,
      editorOption: {},
      newart: true
    };
  },
  components: { quillRedefine },
  created() {
    this.editorOption = quillRedefine({
      // 图片上传的设置
      uploadConfig: {
        action: url + "/api/article/upload/", // 必填参数 图片上传地址
        // 必选参数  res是一个函数，函数接收的response为上传成功时服务器返回的数据
        // 你必须把返回的数据中所包含的图片地址 return 回去
        res: respnse => {
          return respnse.url;
        },
        methods: "POST", // 可选参数 图片上传方式  默认为post
        // token: sessionStorage.token,  // 可选参数 如果需要token验证，假设你的token有存放在sessionStorage
        header: (xhr, formData) => {
          // xhr.setRequestHeader('myHeader','myValue');
          formData.append("username", "123");
        },
        name: "thumbnail", // 可选参数 文件的参数名 默认为img
        size: 4096, // 可选参数   图片限制大小，单位为Kb, 1M = 1024Kb
        accept: "image/png, image/gif, image/jpeg, image/bmp, image/x-icon", // 可选参数 可上传的图片格式
        // start: function (){}
        start: () => {}, // 可选参数 接收一个函数 开始上传数据时会触发
        end: () => {}, // 可选参数 接收一个函数 上传数据完成（成功或者失败）时会触发
        success: () => {}, // 可选参数 接收一个函数 上传数据成功时会触发
        error: () => {} // 可选参数 接收一个函数 上传数据中断时会触发
      },
      // 以下所有设置都和vue-quill-editor本身所对应
      placeholder: "", // 可选参数 富文本框内的提示语
      theme: "snow", // 可选参数 富文本编辑器的风格
      toolOptions: [
        ["bold", "italic", "underline", "strike"], //加粗，斜体，下划线，删除线
        ["blockquote", "code-block"], //引用，代码块

        [{ header: 1 }, { header: 2 }], // 标题，键值对的形式；1、2表示字体大小
        [{ list: "ordered" }, { list: "bullet" }], //列表
        [{ script: "sub" }, { script: "super" }], // 上下标
        [{ indent: "-1" }, { indent: "+1" }], // 缩进
        [{ direction: "rtl" }], // 文本方向
        // [{ size: ["small", false, "large", "huge"] }], // 字体大小
        [{ size: ["small", false, "large", "huge"] }],
        [{ header: [1, 2, 3, 4, 5, 6, false] }], //几级标题

        [{ color: [] }, { background: [] }], // 字体颜色，字体背景颜色
        [{ font: [] }], //字体
        [{ align: [] }], //对齐方式

        ["clean"], //清除字体样式
        ["image", "video"] //上传图片、上传视频
      ], // 可选参数  选择工具栏的需要哪些功能  默认是全部
      handlers: {}
      // 可选参数 重定义的事件，比如link等事件
    });

    this.editorOption.modules.syntax = {
      highlight: text => hljs.highlightAuto(text).value
    };
  },
  computed: {
    editor() {
      return this.$refs.myQuillEditor.quill;
    }
  },
  methods: {
    ckeditor() {
      var form = document.getElementById("go");
      form.submit();
    },
    upload() {
      let self = this;
      let formData = new FormData();
      formData.append("thumbnail", this.$refs.upload.files[0]);
      formData.append("username", self.user.username);
      const instance = this.axios.create({
        withCredentials: true
      });
      instance.post(url + "/api/article/upload/", formData).then(response => {
        if (response.data.code === 200) {
          self.article.thumbnail = response.data.url;
        } else {
          msg(self.$t("lang.article.uploadfail"), "red");
        }
      });
    },
    indexshow() {
      this.article.content = this.content;
      let self = this;
      let art = {};
      this.axios({
        url: url + "/api/index/",
        method: "post",
        data: JSON.stringify({
          article: self.article,
          user: self.user
        }),
        headers: {
          "Content-Type": "application/json"
        }
      }).then(
        function(response) {
          if (response.data.code === 200) {
            msg(self.$t("lang.newart.showsuccess"), "#2ecc71");
          } else if (response.data.code === 400) {
            msg(self.$t("lang.newart.authFail"), "red");
          } else {
            msg("未知错误..", "#FF9966");
            console.log(response.data);
          }
        },
        function(response) {
          msg("未知错误..", "#FF9966");
          console.log(response);
        }
      );
    },
    onEditorReady(editor) {
      // 准备编辑器
    },
    onEditorBlur() {}, // 失去焦点事件
    onEditorFocus() {}, // 获得焦点事件
    onEditorChange() {}, // 内容改变事件
    saveHtml: function(event) {
      alert(this.content);
    },
    addart() {
      this.article.content = this.content;
      let self = this;
      let art = {};
      this.axios({
        url: url + "/api/article/",
        method: "post",
        //发送格式为json
        data: JSON.stringify({
          article: self.article,
          user: self.user
        }),
        headers: {
          "Content-Type": "application/json"
        }
      }).then(
        function(response) {
          if (response.data.code === 200) {
            self.$router.push("/admin/article");
            msg(self.$t("lang.newart.addsuccess"), "#2ecc71");
          } else if (response.data.code === 400) {
            msg(self.$t("lang.newart.authFail"), "red");
          } else if (response.data.code === 401) {
            msg(self.$t("lang.newart.titleHas"), "red");
          } else {
            msg("未知错误..", "#FF9966");
            console.log(response.data);
          }
        },
        function(response) {
          msg("未知错误..", "#FF9966");
          console.log(response);
        }
      );
    },
    change() {
      this.article.content = this.content;
      let self = this;
      this.axios
        .put(
          url + "/api/article/",
          Qs.stringify({
            article: JSON.stringify(self.article),
            user: JSON.stringify(self.user),
            editor: "quill"
          })
        )
        .then(response => {
          if (response.data.code === 200) {
            self.$router.push({ path: "/admin/article" });
          } else if (response.data.code === 400) {
            msg(self.$t("lang.newart.authFail"), "red");
          } else if (response.data.code === 401) {
            msg(self.$t("lang.newart.titleHas"), "red");
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
    let load = loading(document.getElementById("newarticle"));
    if (this.$store.state.user != null) {
      this.user = this.$store.state.user;
    } else {
      this.user = { role: 0 };
    }
    if (localStorage.getItem("auth") != null) {
      this.user = this.$store.state.user;
    } else {
      this.user = { role: 0 };
    }
    let id = this.$route.query.id;
    this.article._id = id;
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
          self.article.category = self.category[0]._id.$oid;
          self.article.thumbnail = self.category[0].thumbnail;
          if (id) {
            this.newart = false;
            this.axios
              .get(url + "/api/article/", {
                params: {
                  _id: id
                }
              })
              .then(response => {
                if (response.data.code === 200) {
                  let obj = JSON.parse(response.data.data);
                  self.article._id = obj._id.$oid;
                  self.article.title = obj.title;
                  self.article.category = obj.category.$oid;
                  self.article.thumbnail = obj.thumbnail;
                  self.article.desc = obj.desc;
                  self.article.author = obj.author;
                  self.content = obj.content;
                } else {
                  console.log(response);
                }
              })
              .catch(response => {
                console.log(response);
              });
          } else {
            this.newart = true;
          }
          document.getElementById("newarticle").removeChild(load);
        } else {
          console.log(response);
        }
      })
      .catch(response => {
        console.log(response);
      });
  },
  watch: {
    // "article.category"(newValue, oldValue) {
    //   for (let i = 0; i < this.category.length; i++) {
    //     if (this.category[i]._id.$oid == newValue) {
    //       this.article.thumbnail = this.category[i].thumbnail;
    //     }
    //   }
    // }
  }
};
</script>

<style lang="scss">
#newarticle {
  background: rgba(0, 0, 0, 0.3);
  padding: 20px;
  border-radius: 6px;
  width: 100%;
  box-sizing: border-box;
  #go1 {
    float: right;
    margin: 5px 20px;
    #editor1 {
      background: rgba(255, 255, 255, 0.4);
      color: #fff;
      border: none;
      border-radius: 4px;
      height: 24px;
      width: 120px;
      cursor: pointer;
      transition: 0.3s;
      &:hover {
        background: rgba(255, 255, 255, 0.2);
      }
    }
  }
  #go2 {
    float: right;
    margin: 5px 20px;
    #editor2 {
      background: rgba(255, 255, 255, 0.4);
      color: #fff;
      border: none;
      border-radius: 4px;
      height: 24px;
      width: 120px;
      cursor: pointer;
      transition: 0.3s;
      &:hover {
        background: rgba(255, 255, 255, 0.2);
      }
    }
  }
  #go3 {
    float: right;
    margin: 5px 20px;
    #editor3 {
      background: rgba(255, 255, 255, 0.4);
      color: #fff;
      border: none;
      border-radius: 4px;
      height: 24px;
      width: 80px;
      cursor: pointer;
      transition: 0.3s;
      &:hover {
        background: rgba(255, 255, 255, 0.2);
      }
    }
  }
  .title {
    width: 100%;
    color: #fff;
    font-size: 24px;
    padding: 15px 15px 15px 0;
    box-sizing: border-box;
    letter-spacing: 2px;
    display: flex;
    justify-content: space-between;
  }
  .pla {
    width: 100%;
    background: rgba(0, 0, 0, 0.4);
    border: none;
    border-bottom: solid 1px #fff;
    margin: 10px 0;
    outline: none;
    color: #fff;
    font-size: 20px;
    padding: 10px 24px;
    box-sizing: border-box;
    border-radius: 4px 4px 0 0;

    &::-webkit-input-placeholder {
      color: rgba(255, 255, 255, 0.5);
      letter-spacing: 1px;
    }
    &:-moz-placeholder {
      color: rgba(255, 255, 255, 0.5);
      letter-spacing: 1px;
    }
    &::-moz-placeholder {
      color: rgba(255, 255, 255, 0.5);
      letter-spacing: 1px;
    }
    &:-ms-input-placeholder {
      color: rgba(255, 255, 255, 0.5);
      letter-spacing: 1px;
    }
  }
  .cate {
    width: 100%;
    background: rgba(0, 0, 0, 0.4);
    border: none;
    border-bottom: solid 1px #fff;
    margin: 10px 0;
    outline: none;
    color: #fff;
    font-size: 20px;
    padding: 10px 20px;
    box-sizing: border-box;
    border-radius: 4px 4px 0 0;
  }
  .thumbnail {
    width: 100%;
    input {
      width: 80%;
    }
    .upload {
      display: inline-block;
      margin-left: 2%;
      width: 18%;
      height: 45px;
      background: rgba(0, 0, 0, 0.6);
      border: none;
      color: #fff;
      transition: 0.6s;
      cursor: pointer;
      border-radius: 4px;
      outline: none;
      text-align: center;
      line-height: 45px;
      &:hover {
        background: rgba(138, 138, 138, 0.5);
        color: #fff;
      }
    }
  }
  .desc {
    width: 100%;
    background: rgba(0, 0, 0, 0.4);
    border: none;
    border-bottom: solid 1px #fff;
    margin: 10px 0;
    outline: none;
    color: #fff;
    font-size: 20px;
    padding: 5px 20px;
    box-sizing: border-box;
    border-radius: 4px 4px 0 0;
    resize: none;
  }
  .opera {
    display: flex;
    justify-content: center;
    button {
      margin: 30px 3% 10px 3%;
      width: 200px;
      height: 50px;
      font-size: 18px;
      background: rgba(0, 0, 0, 0.6);
      border: none;
      color: #fff;
      transition: 0.6s;
      cursor: pointer;
      border-radius: 4px;
      outline: none;
      &:hover {
        background: rgba(138, 138, 138, 0.5);
        color: #fff;
      }
    }
  }
}
#tinymce_ifr {
  background: rgba(255, 255, 255, 0.9);
}
.ql-syntax {
  font-size: 22px;
}
.quill-editor {
  background: #ddd;
}
.ql-toolbar {
  background: #fff;
}
</style>
