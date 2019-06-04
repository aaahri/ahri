<template>
  <div id="indexlast" class="indexlast">
    <p v-for="i in category" @click="goto(i._id)">
      <span class="title">{{i.title}}</span>
      <span class="desc">{{i.desc}}</span>
    </p>
  </div>
</template>

<script>
import msg from "@/assets/tips";
import loading from "@/assets/loading";
import url from "@/assets/server";
import Qs from "qs";
export default {
  name: "indexcate",
  data() {
    return {
      category: []
    };
  },
  methods: {
    goto(id) {
      this.$router.push({ path: "/read", query: { id: id.$oid } });
    }
  },
  mounted() {
    let load = loading(document.getElementById("indexlast"));
    let self = this;
    this.axios
      .get(url + "/api/index/indexlast")
      .then(response => {
        if (response.data.code === 200) {
          self.category = JSON.parse(response.data.data);
          document.getElementById("indexlast").removeChild(load);
        } else {
          msg("未知错误..(from category get 500)", "#FF9966");
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
.indexlast {
  position: relative;
  padding: 15px;
  min-height: 30px;
  p {
    margin: 5px 15px;
    color: #777;
    font-weight: 700;
    transition: 0.4s;
    cursor: pointer;
    &:hover {
      color: #333;
      text-decoration: none;
    }
    &:active {
      color: #000;
    }
    .title {
      display: inline-block;
      width: 200px;
      text-align: right;
      text-decoration: underline;
      &:hover {
        color: #333;
        text-decoration: none;
      }
    }
    .desc {
      display: inline-block;
      text-align: left;
      margin: 0 20px;
      font-size: 12px;
    }
  }
}
</style>
