from django.utils.safestring import mark_safe

class Page:
    def __init__(self,current_page,count,pager_count=10,pager_num=7):
        self.current_page=current_page
        self.count=count
        self.pager_count=pager_count
        self.pager_num=pager_num

    @property
    def start(self):
        return (self.current_page -1) * self.pager_count

    @property
    def end(self):
        return self.current_page * self.pager_count

    @property
    def  all_count(self):
        v, y = divmod(self.count,self.pager_count)
        if y:
            count = v + 1
        return v

    def page_str(self,base_url):
        if self.all_count < self.pager_num:
            start_index = 1
            end_index = self.all_count + 1
        else:
            if self.current_page <= (self.pager_num + 1) / 2:
                start_index = 1
                end_index = self.pager_num + 1
            else:
                start_index = self.current_page - (self.pager_num - 1) / 2
                end_index = self.current_page + (self.pager_num - 1) / 2 + 1
                if (self.current_page + (self.pager_num - 1) / 2) > self.all_count:
                    start_index =self. all_count - 10
                    end_index = self.all_count + 1
        page_list = []
        if self.current_page == 1:
            prev = '<a class="c1" href="javascript:void(0)">上一页</a>'
        else:
            prev = '<a class="c1" href="/%s/?p=%s">上一页</a>' % (base_url,self.current_page - 1)
        page_list.append(prev)
        for i in range(int(start_index), int(end_index)):
            if i == self.current_page:
                tamg = '<a class="c1 active" href="/%s/?p=%s">%s</a>' % (base_url,i, i)
            else:
                tamg = '<a  class="c1" href="/%s/?p=%s">%s</a>' % (base_url,i, i)
            page_list.append(tamg)
        if self.current_page == self.count:
            nex = '<a class="c1" href="javascript:void(0)">下一页</a>'
        else:
            nex = '<a class="c1" href="/%s/?p=%s">下一页</a>' % (base_url,self.current_page + 1)

        page_list.append(nex)
        jump = '''
            <input type="text"/><a onclick='jumpTo(this,"/%s/?p=")'>GO</a>
            <script>
                function jumpTo(ths,base){
                    var val=ths.previousSibling.value;
                    location.href = base + val;
                }
            </script>
        '''% base_url
        page_list.append(jump)
        page_str = ''.join(page_list)
        # print(type(page_str))
        page_str = mark_safe(page_str)
        return page_str