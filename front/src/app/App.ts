import { Component, Prop, Vue } from 'vue-property-decorator';
import DTPNavbar from "@/components/dtp-navbar/DTPNavbar"
import DTPFooter from "@/components/dtp-footer/DTPFooter"


@Component({
    
    components: {
        "dtp-navbar": DTPNavbar,
        "dtp-footer": DTPFooter
    }
})
export default class App extends Vue { }
