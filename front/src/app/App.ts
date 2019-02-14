import { Component, Prop, Vue } from 'vue-property-decorator';
import DNavbar from "@/components/d-navbar/DNavbar"
import DFooter from "@/components/d-footer/DFooter"


@Component({
    components: {
        "dtp-navbar": DNavbar,
        "dtp-footer": DFooter
    }
})
export default class App extends Vue { }
