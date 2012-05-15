from lettuce.django import django_url
from lettuce import before, after, world, step
import sys, time
from selenium.webdriver import ActionChains
from selenium.webdriver.support.select import Select
from mediathread.projects.models import Project

@step(u'There are no projects')
def there_are_no_projects(step):
    assert len(Project.objects.all()) == 0

@step(u'There is an? ([^"]*) ([^"]*) panel')
def there_is_a_state_name_panel(step, state, name):
    """
    Keyword arguments:
    state -- open, closed
    name -- composition, assignment, discussion, collection 

    """
    try:
        panel = world.firefox.find_element_by_css_selector("td.panel-container.%s.%s" % (state.lower(), name.lower()))
    except:
        time.sleep(1)
        panel = world.firefox.find_element_by_css_selector("td.panel-container.%s.%s" % (state.lower(), name.lower()))
    assert panel != None, "Can't find panel named %s" % panel
    
@step(u'the ([^"]*) panel has a ([^"]*) button')
def the_panel_has_a_name_button(step, panel, name):
    panel = world.firefox.find_element_by_css_selector("td.panel-container.open.%s" % panel.lower())
    assert panel != None, "Can't find panel named %s" % panel
    
    btn = world.find_button_by_value(name, panel)
    assert btn != None, "Can't find button named %s" % name
    
@step(u'I call the ([^"]*) "([^"]*)"')
def i_call_the_composition_title(step, panel, title):
    panel = world.firefox.find_element_by_css_selector("td.panel-container.open.%s" % panel.lower())
    assert panel != None, "Can't find panel named %s" % panel
    
    input = panel.find_element_by_name("title")
    input.clear()
    input.send_keys(title)
    
@step(u'I write some text for the ([^"]*)')
def i_write_some_text_for_the_composition(step, panel):
    panel = world.firefox.find_element_by_css_selector("td.panel-container.open.%s" % panel.lower())
    assert panel != None, "Can't find panel named %s" % panel
    
    frame = panel.find_element_by_tag_name("iframe")
    world.firefox.switch_to_frame(frame)
    input = world.firefox.find_element_by_class_name("mceContentBody")
    input.send_keys("""The Columbia Center for New Teaching and Learning was (CCNMTL)
                    was founded at Columbia University in 1999 to enhance teaching and
                    learning through the purposeful use of new media and technology""")
    
    world.firefox.switch_to_default_content()

@step(u'I see a ([^"]*) dialog')
def i_see_a_name_dialog(step, name):
    elt = world.firefox.find_element_by_css_selector('span.ui-dialog-title')
    assert elt != None and elt.text == "Save Changes"
    
@step(u'the project visibility is "([^"]*)"')
def the_project_visibility_is_level(step, level):
    elt = world.firefox.find_element_by_id('id_publish')
    assert elt != None, "Cannot locate project visibility options"
    
    select_box = Select(elt)
    selected = select_box.first_selected_option
    assert selected.text == level, "Expect visibility to be like %s. Instead it is %s" % (level, value)
    
@step(u'There is a project visibility "([^"]*)"')
def there_is_a_project_visibility_level(step, level):
    elt = world.firefox.find_element_by_id('id_publish')
    assert elt != None, "Cannot locate project visibility options"
    
    select_box = Select(elt)
    for o in select_box.options:
        if o.text.strip() == level:
            return
    
    assert False, "No %s option found" % (level)
    
@step(u'Then I set the project visibility to "([^"]*)"')
def i_set_the_project_visibility_to_visibility(step, visibility):
    elt = world.firefox.find_element_by_id('id_publish')
    assert elt != None, "Cannot locate project visibility options"
    
    select_box = Select(elt)
    select_box.select_by_visible_text(visibility)
    
@step(u'Then there are ([0-9][0-9]?) projects')
def then_there_are_count_projects(step, count):
    elts = world.firefox.find_elements_by_css_selector("li.projectlist")
    assert len(elts) == int(count), "There are %s projects. Expected %s"  % (len(elts), count)
    
@step(u'i save the changes')
def i_save_the_changes(step):
    elts = world.firefox.find_elements_by_tag_name("button")
    for e in elts:
        if e.get_attribute("type") == "button" and e.text == "Save":
            e.click()
            time.sleep(1)
            return
        
    assert False, "Unable to locate the dialog's save button"
    
@step(u'there is a ([^"]*) "([^"]*)" project by ([^"]*)')
def there_is_a_status_title_project_by_author(step, status, title, author):
    elts = world.firefox.find_elements_by_css_selector("li.projectlist")
    assert len(elts) > 0, "Expected to find at least 1 project. Instead there are none"
    for e in elts:
        title_elt = e.find_element_by_css_selector("a.asset_title.type-project")
        if title_elt.text.strip() == title:
            # author
            author_elt = e.find_element_by_css_selector("span.metadata-value-author")
            msg = "%s author is [%s]. Expected [%s]." % (title, author_elt.text.strip(), author)
            assert author_elt.text.strip() == author, msg
                
            # status            
            status_elt = e.find_element_by_css_selector("span.metadata-value-status")
            msg = "%s status starts with [%s]. Expected [%s]" % (title, status_elt.text.strip().lower(), status)
            assert status_elt.text.strip().lower().startswith(status), msg 
            
            return
            
    assert False, "Unable to find project named %s" % title